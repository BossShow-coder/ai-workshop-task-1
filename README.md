# AI-Assisted Development Workshop: Challenge 1

Welcome to the build session! Before you start building your application, you need to reveal your secret mission.

## Your Task

Your final application requirements are hidden inside an encrypted file in this repository. Your first objective is to build a Python script that decrypts this message.

### Files in this Repository

- `challenge/encrypted_spec.txt`: The encrypted specification (a Fernet token).
- `challenge/crypto_key.txt`: The secret key required for decryption.

## Instructions for Challenge 1

1.  **Work with AI**: Use your AI coding assistant (like Roo Code) to write a python script to decrypt your specific mission.
2.  **The Goal**: The script must read the key from `challenge/crypto_key.txt` and the encrypted message from `challenge/encrypted_spec.txt`, then print the decrypted text to the console.
3.  **Hint**: The message was encrypted using the **Fernet** symmetric encryption scheme from the `cryptography` Python library.

### Success Criteria
When you run `python decrypt.py`, you should see:
1. A Title for your app.
2. A "One-Liner" description.
3. 5 high-level functional requirements (bullet points).

---

## Challenge 2: The Main Build

Once you have successfully decrypted your specification, you are ready to build the app! 


### Step 1: Initialize Your Own Repository

To track your progress and share your final build, you need to create your own GitHub repository.

1.  **Create on GitHub**: Go to [github.com/new](https://github.com/new).
    - Repository Name: (Something relevant to your app title)
    - Visibility: **Public** (required for the show-and-tell)
    - **Do NOT** initialize with a README (we will push everything).
2.  **Clone to a New Folder**:
    - Open a terminal and move to your projects directory.
    - Run: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
3.  **Move Your Files**:
    - Copy your specification into your new repository folder. Any way you like : create a .txt or just paste it for AI and tell it to "create me a specification document". 
    > **Hint:** Let the AI expand on the short specification and create a more elaborate specification.
    >
    > **Hint:** Let AI store the specification in your repository.
4.  **First Commit**:
    - `git add .`
    - `git commit -m "Initial commit: Challenge 1 decrypted"`
    - `git push origin main`

### Step 2: Build the App with AI

Now, build the application described in your decrypted specification. 

- **Commit Often**: Every time you reach a milestone (e.g., "UI working", "Logic implemented"), do a git commit.
- **Goal**: Have a working application and a clean commit history by the end of the session.
> **Hint:** Choose a small iteration and get "something" running so you can iterate quickly.

---
## AI Hints

It can be helpful to tell ROO/ZOO to follow a specific tech stack before beginning work.
For example - paste something like the below System Prompt in your roo config (easiest) 
(OR in .roo/ folder to make it project specific, this a bit more work, ask for help if needed)

> **System prompt:**
- Build in python, create single container apps, use FastAPI, separate HTML, and leverage CSS plus frontend components such as Tailwind, Leaflet, Vue, etc., where applicable.
- Prefer this configuration when planning the solution.
- Whenever choosing frontend components, prefer loading them from public CDNs and ask the user before switching to in-repo or self-hosted delivery methods.
- For basic database or caching use local files and for anything more than one object or table, use SQLite.

---
*Questions? Contact the workshop facilitator.*
