# vLLM 
- [Documentação](https://docs.vllm.ai/en/latest/)
- [Github](https://github.com/vllm-project/vllm)

O Projeto vLLM é desenvolvido [Sky Computing Lab at UC Berkeley](https://sky.cs.berkeley.edu/) e foi pelo foi escolhido pelos principais pontos:

- Servidor compatível com sdk/endpoints da OpenAI
- Integração direta com os modelos do HuggingFace
- [Geração guiada](https://docs.vllm.ai/en/v0.8.4/features/structured_outputs.html)
- Possibilidade de inferência distribuida (Tensor, pipeline, data and expert parallelism)
- Funcionalidades adicionais:
    - Efficient management of attention key and value memory with PagedAttention
    - Continuous batching of incoming requests
    - Fast model execution with CUDA/HIP graph
    - Quantizations: GPTQ, AWQ, AutoRound, INT4, INT8, and FP8
    - Optimized CUDA kernels, including integration with FlashAttention and FlashInfer
    - Speculative decoding
    - Chunked prefill
