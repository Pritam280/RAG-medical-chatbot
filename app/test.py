
from app.components.llm import load_llm

llm = load_llm()

response = llm.invoke(
    "Explain Kubernetes in two simple sentences."
)

print(response.content)
