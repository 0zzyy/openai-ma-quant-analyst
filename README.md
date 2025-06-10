# openai-ma-quant-analyst
ChatGPT based software to analyze Definitive Merger and Acquisition Letters and predict the success rate 

# M&A Quantitative Analyst AI Playground Config

This repo contains everything you need to paste directly into OpenAI Playground:

- **System Message**  
- **Functions JSON**  
- **Playground Settings**

## Usage

1. Open **OpenAI Playground**.
2. In the **System** box, paste the **System Message** from `playground_config.md`.
3. In the **Functions** pane, paste the **Functions JSON** from `playground_config.md` (as an array).
4. In **Settings**, use:
   - **Model:** gpt-4.1  
   - **Response format:** text  
   - **Tool choice:** auto  
   - **Temperature:** 1.00  
   - **Max tokens:** 2048  
   - **Top_p:** 1.00  
   - **Store:** false  
5. Make your calls to any of the defined functions!

---

All details in **playground_config.md** below.
