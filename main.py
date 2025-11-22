from parent_agent import TourismAgent

if __name__ == "__main__":
    agent = TourismAgent()
    while True:
        msg = input("You: ")
        if msg.lower().strip() in ['exit', 'quit']:
            print("AI: Goodbye!")
            break
        print("AI:", agent.handle(msg))
