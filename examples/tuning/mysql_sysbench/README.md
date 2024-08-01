1. Prepare the environment
```bash
sh prepare.sh
```
if running failed, you may try to install mysql and sysbench manually according to following guide:
- Install MySQL according to the guide ([https://blog.csdn.net/weixin_43214408/article/details/116895091](https://blog.csdn.net/weixin_43214408/article/details/116895091))
- Install sysbench according to the guide ([https://blog.csdn.net/weixin_43214408/article/details/116898751](https://blog.csdn.net/weixin_43214408/article/details/116898751))

2. Start to tuning
```bash
atune-adm tuning --project mysql_sysbench --detail mysql_sysbench_client.yaml
```

3. Restore the environment
```bash
atune-adm tuning --restore --project mysql_sysbench
```

**extra guide**

 请确保您在运行本调优程序前，已经配置好mysql和sysbench，并将该目录下的my.cnf文件内容附加到您的my.cnf文件末尾，这些是调优时调整的参数，如果您的配置文件中没有这些项目，则无法进行相应的调优。

 开始调优前，请修改本目录下的sysbench_config.cfg文件，确保您输入了mysql的正确密码，否则sysbench可能无法正常运行。
如果sysbench执行过程中出现死锁或段错误，可以尝试降低并发数。

