import yaml
data = {'train' : './train/images',
        'test' : './test/images',
        'val' : './valid/images',
        'nc': 2,
        'names': ['normal','error']
}

with open('./datasets/cobot_control/custom_data.yaml', 'w') as f:
  yaml.dump(data, f)