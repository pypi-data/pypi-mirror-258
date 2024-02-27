import json

from openai import OpenAI

info = """
Your task is iterative code optimization.

1. The user gives you the initial [code, result] pair as the baseline,
    meanwhile demonstrating you the interfaces.
    You are only given the part of code that you need to optimize,
    so assume everything given to you is used and don't worry about missing definitions!
2. You send back some improved code based on your understanding, knowledge and expertise.
    You should provide your observations, learnings and explanations,
    but keep your reply short and concise, focus on the essentials!!!
    You should put your improved code inside <NewCode></NewCode> special tags so the user
    can extract the code and execute it.
3. The user will send back to you the result of your new code,
    and then you repeat step 2 for this iterative optimization process.
    This means you need to learn from all the [code, result] pairs starting from baseline.
    But note that the goal is to generate better code than the baseline,
    not better code than the ones you have produced yourself!!!
    Always check if your latest result is better than the baseline (or last best result)!
"""


class CodeOptimizer:
    def __init__(s, api_key, model="gpt-4"):
        s.ai = OpenAI(api_key=api_key)
        s.model = model
        s.messages = [{"role": "system", "content": info}]
        s.json_path = "CodeOptimizer.json"
        s.md_path = "CodeOptimizer.md"
        try:
            with open(s.json_path) as f:
                s.messages = json.load(f)
        except Exception:
            pass

    def set_baseline(s, code, result):
        user_content = f"""
The following baseline code
<BaseCode>
{code}
</BaseCode>
gives the following result:
{result}
"""
        return s.get_code(user_content)

    def feedback(s, result):
        user_content = f"""
Your previews new code gives the following result:
{result}
"""
        return s.get_code(user_content)

    def get_code(s, user_content):
        ai_content = s.call_ai(user_content)
        code = ai_content.split("<NewCode>")[1].split("</NewCode>")[0]
        return code

    def call_ai(s, user_content):
        user_msg = {"role": "user", "content": user_content}
        s.messages.append(user_msg)

        ai_content = (
            s.ai.chat.completions.create(
                model=s.model,
                messages=s.messages,
                temperature=0.7,
                # max_tokens=256,
                top_p=1,
            )
            .choices[0]
            .message.content
        )
        ai_msg = {"role": "assistant", "content": ai_content}
        s.messages.append(ai_msg)
        with open(s.md_path, "w+") as f:
            json.dump(s.messages, f)
        with open(s.md_path, "w+") as f:
            f.write("\n\n".join([f"{x['role']}:\n{x['content']}" for x in s.messages]))
        return ai_content
