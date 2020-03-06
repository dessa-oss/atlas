# RAPIDS

**Requirements**: NVIDIA GPU, Pascal or better with compute capability of 6.0+

[RAPIDS](https://developer.nvidia.com/rapids) is a set of software libraries for data science on GPUs. RAPIDS implements interfaces that are similar to pandas, scikit-learn, and others, enabling you to convert preprocessing and machine learning code to run orders of magnitude faster with relatively minimal code changes. Why limit your GPUs to just doing deep learning modeling? 

## Test a baseline

Create a `preprocessing_test.py`

```python
import pandas as pd
import numpy as np
import time
import foundations

DF1_SIZE = int(2e5)
DF2_SIZE = int(1e4)
DF3_SIZE = int(1e6)

def random_dataframe(num_rows):
    df = pd.DataFrame()

    print("Creating {}-row dataframe".format(num_rows))
    df['col_a'] = np.random.choice(['a', 'b', 'c', 'd'], num_rows)
    df['col_b'] = np.random.randint(0, 10, num_rows)
    df['col_c'] = np.random.randint(0, 5, num_rows)
    df['col_d'] = np.random.randint(0, 3, num_rows)
        
    return df

df1 = random_dataframe(DF1_SIZE)
df2 = random_dataframe(DF2_SIZE)
df3 = pd.DataFrame(np.random.random((DF3_SIZE, 3)))

print("df1 df2 merging")
start_time = time.time()
df1.merge(df2, on='col_b', how='inner')
foundations.log_metric("join time", "{:.4f}".format(time.time() - start_time))

print("df3 sorting")
start_time = time.time()
df3.sort_values(by=list(df3))
foundations.log_metric("sort time", "{:.4f}".format(time.time() - start_time))
```

Run our script

```bash
python preprocessing_test.py 
```

## Create a RAPIDS Docker image for Atlas


First, create a `requirements.txt`

```
wheel
request
jsonschema
dill==0.2.8.2
redis==2.10.6
pandas==0.23.3
google-api-python-client==1.7.3
google-auth-httplib2==0.0.3
google-cloud-storage==1.10.0
PyYAML==5.1.2
pysftp==0.2.8
paramiko==2.4.1
mock==2.0.0
freezegun==0.3.8
boto3==1.9.86
boto==2.49.0
flask-restful==0.3.6
Flask==1.1.0
Werkzeug==0.15.4
Flask-Cors==3.0.6
mkdocs==1.0.4
promise==2.2.1
pyarmor==5.5.6
slackclient==1.3.0
scikit-learn==0.21.3
xgboost==0.90
```


Once we have that create a new `Dockerfile`:

```Dockerfile
FROM rapidsai/rapidsai:cuda10.0-runtime-ubuntu18.04

COPY requirements.txt /tmp
RUN /opt/conda/envs/rapids/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
        && rm /tmp/requirements.txt

ENTRYPOINT ["/opt/conda/envs/rapids/bin/python"]
```

Save this as a text file named `Dockerfile`. This image will define the environment in which we are going to run jobs. Learn more about Docker [here](https://www.docker.com). 

(if you need to use a version of CUDA, you can find a different Docker parent image [here](https://rapids.ai/start.html) and replace the first line of the `Dockerfile` appropriately)


Now we just run

```
$ docker build . --tag rapidsai-atlas:latest
```

(using `sudo` only if necessary for your Docker setup)



## Create or modify a job.config.yaml

Edit your `job.config.yaml` file if you have one, or create a new one. Add (or modify if appropriate) the following lines:

```yaml
num_gpus: 1
```

and

```yaml
worker:
  image: rapidsai-atlas:latest
```

## Modify our baseline code to use cuDF

Open `preprocessing_test.py` in an editor and make the following changes:

Under

```python
import pandas as pd
import numpy as np
import time
import foundations
```

add

```
import cudf

foundations.log_param('cuDF version', cudf.__version__)
```

Under

```
df1 = random_dataframe(DF1_SIZE)
df2 = random_dataframe(DF2_SIZE)
df3 = pd.DataFrame(np.random.random((DF3_SIZE, 3)))
```

add

```
df1 = cudf.from_pandas(df1)
df2 = cudf.from_pandas(df2)
df3 = cudf.from_pandas(df3)
```


Done! All we had to do was convert our pandas DataFrames to cuDF DataFrames. The standard interfaces are mostly the same. 



Now run the following to submit your code to the scheduler using the custom Docker image that we created above.

```bash
foundations submit scheduler . main.py
```

Go back to the Atlas dashboard. Because we logged `cuDF version` as a parameter, you can check which job used `cuDF`. Compare the metrics and runtimes! 

The cuDF job's recorded times (and overall runtime) should be way faster!

