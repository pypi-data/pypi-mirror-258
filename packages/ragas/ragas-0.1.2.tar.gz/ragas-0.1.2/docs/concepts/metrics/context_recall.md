

# Context Recall

Context recall measures the extent to which the retrieved context aligns with the annotated answer, treated as the ground truth. It is computed based on the `ground truth` and the `retrieved context`, and the values range between 0 and 1, with higher values indicating better performance.

To estimate context recall from the ground truth answer, each sentence in the ground truth answer is analyzed to determine whether it can be attributed to the retrieved context or not. In an ideal scenario, all sentences in the ground truth answer should be attributable to the retrieved context.

The formula for calculating context recall is as follows:

```{math}
\text{context recall} = {|\text{GT sentences that can be attributed to context}| \over |\text{Number of sentences in GT}|}
```

```{hint}

Question: Where is France and what is it's capital?

Ground truth: France is in Western Europe and its capital is Paris. 

High context recall: France, in Western Europe, encompasses medieval cities, alpine villages and Mediterranean beaches. Paris, its capital, is famed for its fashion houses, classical art museums including the Louvre and monuments like the Eiffel Tower.
    Explanation: The context answers both: (1) Where is France: Western Europe, (2) what is it's capital: Paris

Low context recall: France, in Western Europe, encompasses medieval cities, alpine villages and Mediterranean beaches. The country is also renowned for its wines and sophisticated cuisine. Lascaux’s ancient cave drawings, Lyon’s Roman theater and the vast Palace of Versailles attest to its rich history.
    Explanation: The context answers only: (1) Where is France: Western Europe, but not (2) what is it's capital: Paris

```


## Example

```{code-block} python
:caption: Context recall with batch_size 10
from ragas.metrics import ContextRecall
context_recall = ContextRecall(
    batch_size=10

)
# Dataset({
#     features: ['contexts','ground_truth'],
#     num_rows: 25
# })
dataset: Dataset

results = context_recall.score(dataset)
```