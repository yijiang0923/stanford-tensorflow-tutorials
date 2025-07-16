import Foundation

struct ChatMessage: Codable, Identifiable {
    let id = UUID()
    let role: String // "user" or "assistant"
    let content: String
    let timestamp: Date?
    
    enum CodingKeys: String, CodingKey {
        case role, content, timestamp
    }
}

struct ChatRequest: Codable {
    let message: String
    let conversation_history: [ChatMessage]
}

struct ChatResponse: Codable {
    let response: String
    let timestamp: Date
}