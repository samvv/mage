import XCTest
import SwiftTreeSitter
import TreeSitterMage

final class TreeSitterMageTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_mage())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Mage grammar")
    }
}
