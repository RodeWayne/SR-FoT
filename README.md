# SR-FoT
This is the official implementation of the paper "[SR-FoT: A Syllogistic-Reasoning Framework of Thought for Large Language Models Tackling Knowledge-based Reasoning Tasks](https://ojs.aaai.org/index.php/AAAI/article/view/33666)" (AAAI 2025). 

![SR-FoT_pipeline](pipeline/SR-FoT_pipeline.png)

SR-FoT is a 5-stage Framework of Thought based on the Syllogistic-Reasoning paradigm (as shown in the figure above), requiring no training. Its purpose is to guide Large Language Models (LLMs) to perform syllogistic deductive reasoning, thereby enhancing their reasoning capabilities, particularly the rigor of reasoning. We validated the advantages of our method over approaches like Chain-of-Thought (CoT),  on knowledge-based reasoning and question-answering tasks using several state-of-the-art (both closed-source and open-source) LLMs at the time.


## Requirements

First, download and set up the repo:

```setup
git clone https://github.com/RodeWayne/SR-FoT.git
cd SR-FoT
```

## Citation

If you find this code useful in your research, please consider citing:

``` citation
@inproceedings{wan2025sr,
  title={SR-FoT: A Syllogistic-Reasoning Framework of Thought for Large Language Models Tackling Knowledge-based Reasoning Tasks},
  author={Wan, Wentao and Yang, Zhuojie and Chen, Yongcan and Luo, Chenglin and Wang, Ruilin and Cai, Kehao and Kang, Nan and Lin, Liang and Wang, Keze},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={39},
  number={14},
  pages={15186--15194},
  year={2025}
}
```

