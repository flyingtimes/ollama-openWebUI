
## 在cursor中使用下面的prompt，可以将任意格式文件转换成chat_template

请写一个python程序，并实现下面功能：
1、从命令行参数中读取程序的输入文件名
2、读取输入文件中的每一行信息，并将每一行的内容进行转换，并写入输出文件名。
3、输入文件中的每一行的内容格式如下：
{"text": "<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\n\"阿猛，如果你要cos一个角色，你会选择谁呢？\"<|im_end|>\n<|im_start|>assistant\n阿猛可以cos大嫂吗 或者缸灿团队来cos个狂飙想看！！[星星眼][星星眼][星星眼]<|im_end|>"}
4、将每一行的内容转换成下面的格式：
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "阿猛，如果你要cos一个角色，你会选择谁呢？"}, {"role": "assistant", "content": "阿猛可以cos大嫂吗 或者缸灿团队来cos个狂飙想看！！[星星眼][星星眼][星星眼]"}]}
