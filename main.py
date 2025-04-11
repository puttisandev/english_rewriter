from chains import build_chain
from prompts import style_prompts

def rewrite_one_style(user_text: str):
    styles = [k for k in style_prompts.keys() if k != "default"]

    print("\nAvailable styles:")
    for idx, style in enumerate(styles, 1):
        print(f"{idx}. {style}")
    print(f"{len(styles)+1}. custom ✍️")

    selected = input(f"Choose style [1-{len(styles)+1}]: ").strip()

    try:
        selected_idx = int(selected) - 1
        if 0 <= selected_idx < len(styles):
            user_style = styles[selected_idx]
            style_instruction = style_prompts.get(user_style, "")
        elif selected_idx == len(styles):
            # custom style
            custom_instruction = input("Enter your custom style instruction: ")
            user_style = "custom"
            style_instruction = " " + custom_instruction.strip()
        else:
            raise ValueError
    except ValueError:
        print("❌ Invalid selection. Using 'default'")
        user_style = "default"
        style_instruction = ""

    chain = build_chain(style_instruction)
    result = chain.invoke({"text": user_text, "style": style_instruction})

    print(f"\n🎯 Style: {user_style.capitalize()}\n➡ {result}")


def rewrite_all_styles(user_text: str):
    print("\n🧪 Rewriting in multiple styles:\n" + "-" * 40)
    for style_key, style_instruction in style_prompts.items():
        if style_key == "default":
            continue
        chain = build_chain(style_instruction)
        result = chain.invoke({"text": user_text, "style": style_instruction})
        print(f"\n🎯 Style: {style_key.capitalize()}\n➡ {result}")


def main():
    print("🔁 English Rewriter (Type 'exit' or 'quit' to stop)\n" + "-" * 40)
    while True:
        user_text = input("\nEnter your sentence: ").strip()
        if user_text.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        print("\nChoose mode:")
        print("1 = Rewrite with one style")
        print("2 = Rewrite with all styles")
        mode = input("Mode (1 or 2): ").strip()

        if mode == "1":
            rewrite_one_style(user_text)
        elif mode == "2":
            rewrite_all_styles(user_text)
        else:
            print("❌ Invalid mode selected.")


if __name__ == "__main__":
    main()
