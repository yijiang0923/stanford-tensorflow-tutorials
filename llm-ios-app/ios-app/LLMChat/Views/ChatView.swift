import SwiftUI

struct ChatView: View {
    @StateObject private var llmService = LLMService()
    @State private var messages: [ChatMessage] = []
    @State private var inputText = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    @State private var isServerConnected = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Connection status
                if !isServerConnected {
                    HStack {
                        Image(systemName: "wifi.slash")
                            .foregroundColor(.red)
                        Text("Server disconnected")
                            .font(.caption)
                            .foregroundColor(.red)
                        Spacer()
                        Button("Retry") {
                            checkServerConnection()
                        }
                        .font(.caption)
                        .foregroundColor(.blue)
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                    .background(Color.red.opacity(0.1))
                }
                
                // Chat messages
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(messages) { message in
                                MessageBubble(message: message)
                            }
                            
                            if isLoading {
                                HStack {
                                    ProgressView()
                                        .scaleEffect(0.8)
                                    Text("Thinking...")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .padding()
                            }
                        }
                        .padding()
                    }
                    .onChange(of: messages.count) { _ in
                        if let lastMessage = messages.last {
                            withAnimation(.easeInOut(duration: 0.5)) {
                                proxy.scrollTo(lastMessage.id, anchor: .bottom)
                            }
                        }
                    }
                }
                
                // Input area
                VStack {
                    if let errorMessage = errorMessage {
                        Text(errorMessage)
                            .font(.caption)
                            .foregroundColor(.red)
                            .padding(.horizontal)
                    }
                    
                    HStack {
                        TextField("Ask me anything...", text: $inputText, axis: .vertical)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .lineLimit(1...5)
                            .onSubmit {
                                sendMessage()
                            }
                        
                        Button(action: sendMessage) {
                            Image(systemName: "arrow.up.circle.fill")
                                .font(.title2)
                                .foregroundColor(inputText.isEmpty ? .gray : .blue)
                        }
                        .disabled(inputText.isEmpty || isLoading)
                    }
                    .padding()
                }
                .background(Color(UIColor.systemBackground))
            }
            .navigationTitle("Desktop LLM")
            .navigationBarTitleDisplayMode(.inline)
            .navigationBarItems(trailing: Button("Clear") {
                clearChat()
            })
        }
        .onAppear {
            checkServerConnection()
        }
    }
    
    private func sendMessage() {
        guard !inputText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        
        let userMessage = ChatMessage(
            role: "user",
            content: inputText,
            timestamp: Date()
        )
        
        messages.append(userMessage)
        let messageToSend = inputText
        inputText = ""
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await llmService.sendMessage(messageToSend, history: messages)
                
                await MainActor.run {
                    let assistantMessage = ChatMessage(
                        role: "assistant",
                        content: response,
                        timestamp: Date()
                    )
                    messages.append(assistantMessage)
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    errorMessage = "Failed to send message: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }
    }
    
    private func clearChat() {
        messages.removeAll()
        errorMessage = nil
    }
    
    private func checkServerConnection() {
        Task {
            do {
                let isConnected = try await llmService.checkServerHealth()
                await MainActor.run {
                    isServerConnected = isConnected
                }
            } catch {
                await MainActor.run {
                    isServerConnected = false
                }
            }
        }
    }
}