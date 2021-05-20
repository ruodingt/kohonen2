# Kohonen Challenge


![](vlog2.gif)

Please see [kohonen.ipynb](kohonen.ipynb) for the show case

# Run Demo (for fun)
```
docker build -t kohonen2 .
docker run -p 8888:8888 kohonen2 
```

# Run training (for big/serious job)
## with container
```bash
docker run kohonen2 ksom train --config-file "configs/exp1.yaml"
# or running in interactive mode
docker run -it kohonen2 ksom train --config-file "configs/exp1.yaml"
```

## without container

```bash
pip3 install -e .
ksom train --config-file "configs/exp1.yaml"
```
If config_file is not provided it will use default configuration



# Design Thinking

For simplicity this project is mainly using `numpy`

## Feature Summary:
1. **experiment as yaml**: all the experiment configs should goes here
2. **Modular design**: 3 major module - [Trainer](ksom/trainer.py), Model & Dataset.
Trainer is the coordinator of the entire training job.
3. **extensible**: Modules are highly extensive - one may extend their own CustomDataset based on `Dataset` 
(see [dataset.py](ksom/dataset.py)); one may also extend `Hook` ()
3. **cli interface (easy, lazy)**: see section *Run training* above, useless but fun
4. **vlog system (Visibility makes models more explainable)**: take a photo of current weight 
every N steps (defined as `cfg.CALLBACK_PERIOD`). 
[Vlog](ksom/hooks.py) output is saved to `project_root/logs/${exp_name}`
exp_name is same as `.yaml` config filename

```
|---configs: containing yaml file for different experiment settings
|---ksom: main folder of source code
    |---config.py: yaml configuration system
    |---dataset.py: Dataset that generate random colors
    |---default_setup.py: setting for training job and prepare confiigurations
    |---entry.py: connect cli to python program
    |---hooks.py: the callback used during training, can be extended to log iter time, logging, periodic checkpoint 
    |---kohonensom_model.py: the actual model
    |---logger.py: logging system
    |---trainer.py: defining Trainer - the coordinator of the training ob
|---Dockerfile:
|---setup.py: 
```

# Acknowledgement & Reference
- Thanks [@Eliiza](https://eliiza.com.au/) for providing the instruction.
- There are many good implementation of SOM on the Internet. e.g. [[1]](https://medium.com/kirey-group/self-organizing-maps-with-fast-ai-step-1-implementing-a-som-with-pytorch-80df2216ede3)


# Coming soon
- Test & CI
- Periodic Checkpoint Manager (as a Hook)
- attach volume such that logs can be saved in a directory that host can access

# Contact
[Rod (Ruoding) Tian](https://github.com/ruodingt)

ruodingt@gmail.com

+61 422755619

[LinkedIn](https://www.linkedin.com/in/ruodingt-tian/)