import Foundation
import PDFKit
import Vision

struct OCRLine {
    let text: String
    let minX: CGFloat
    let minY: CGFloat
}

func render(page: PDFPage, scale: CGFloat = 2.0) -> CGImage? {
    let bounds = page.bounds(for: .mediaBox)
    let width = Int(bounds.width * scale)
    let height = Int(bounds.height * scale)
    let colorSpace = CGColorSpaceCreateDeviceRGB()

    guard let context = CGContext(
        data: nil,
        width: width,
        height: height,
        bitsPerComponent: 8,
        bytesPerRow: 0,
        space: colorSpace,
        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
    ) else {
        return nil
    }

    context.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.saveGState()
    context.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: context)
    context.restoreGState()
    return context.makeImage()
}

func extractText(from image: CGImage) throws -> String {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["en-US"]

    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    try handler.perform([request])

    let observations = (request.results as? [VNRecognizedTextObservation]) ?? []
    let lines = observations.compactMap { observation -> OCRLine? in
        guard let candidate = observation.topCandidates(1).first else {
            return nil
        }
        return OCRLine(
            text: candidate.string,
            minX: observation.boundingBox.minX,
            minY: observation.boundingBox.minY
        )
    }

    return lines
        .sorted {
            let yDelta = abs($0.minY - $1.minY)
            if yDelta > 0.015 { return $0.minY > $1.minY }
            return $0.minX < $1.minX
        }
        .map(\.text)
        .joined(separator: "\n")
}

guard CommandLine.arguments.count >= 2 else {
    fputs("usage: tmp_pdf_ocr.swift <pdf-path> [pages]\n", stderr)
    exit(2)
}

let pdfPath = CommandLine.arguments[1]
let maxPages = CommandLine.arguments.count >= 3 ? (Int(CommandLine.arguments[2]) ?? 2) : 2

guard let document = PDFDocument(url: URL(fileURLWithPath: pdfPath)) else {
    fputs("failed to open pdf: \(pdfPath)\n", stderr)
    exit(1)
}

for index in 0..<min(document.pageCount, maxPages) {
    guard let page = document.page(at: index),
          let image = render(page: page) else {
        continue
    }
    print("PAGE \(index + 1)")
    do {
        print(try extractText(from: image))
    } catch {
        fputs("ocr failed on page \(index + 1): \(error)\n", stderr)
    }
    print("\n---PAGE BREAK---\n")
}
