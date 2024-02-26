# sessionGPT

Just for fun utility to generate AWS IAM session policies using GPT-4.

### Install
```
pip install sessiongpt
```

### Example Usage

```sh
sessiongpt --description "I want to create and manage S3 buckets, update my Lambda memory configuration. I also need to perform all database actions, but I don't want to delete any by accident." --pretty
```
