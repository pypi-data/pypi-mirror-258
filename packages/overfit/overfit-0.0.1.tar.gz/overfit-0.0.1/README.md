# overfit
ML training code generator. Not ready for use.

## Examples
```python
from overfit.unsupervised import UnsupervisedPipeline
fit = UnsupervisedPipeline(data = data,
                         target = 'target_name',
                         type = 'kmeans',
                         nfolds = 10
                         )
# fit.get_code(), print
fit.code_gen() # run

```