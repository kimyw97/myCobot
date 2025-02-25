import yaml
data = {'train' : './error_dectection/train/images',
        'test' : './error_dectection/test/images',
        'val' : './error_dectection/valid/images',
        'nc': 2,
        'names': ['normal','error']
}

with open('./datasets/error_detection/custom_data.yaml', 'w') as f:
  yaml.dump(data, f)