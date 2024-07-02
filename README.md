This is my glorious attempt to understand the Mistral 7B model. Because the people from Mistral AI have open-sourced their model code, I tried to replicate a small version of the model. Like... really small. A whopping a million parameters. Needless to say, the model is useless for anything. 

The model was trained on a handful examples from the Cosmopedia dataset, which is an open-source version of the high quality textbook dataset in a similar style to the Phi dataset.

Check out the model here: 
https://huggingface.co/LeonardPuettmann/MiniMistral-8M

### Loss 
The loss is pretty unspectacular. I just trained for one epoch:
![Loss Curve](logs/loss.png)

### How to use
Please don't. You should probably use Mistral 7B instead: [mistralai/Mistral-7B-v0.3](https://huggingface.co/mistralai/Mistral-7B-v0.3)
Or if you are (very) GPU rich, you can try to train their model yourself: https://github.com/mistralai/mistral-inference

In the folder `inference` you actually find a small script, which allows you to chat with the 7B param model. All you need is a free HuggingFace API token.