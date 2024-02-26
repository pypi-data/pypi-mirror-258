import os

root_dir = "E:/ml/sharaborno"

configs = {
    "batch_size": 64,
    "epochs": 10,
    "steps_per_epoch": 100,
    "validation_steps": 20,
    "max_tokens": 10000,
    "units": 256,
    "buffer_size": 100000,
    'model_dir': os.path.join(root_dir, 'saved_models'),
    'data_dir': os.path.join(root_dir, 'datasets'),
}
