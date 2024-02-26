#include <torch/extension.h>
#include <cuda_runtime.h>
#include <cstdint>
#include <ATen/ATen.h>
#include <ATen/Context.h>
#include <ATen/cuda/CUDAContext.h>
#include <cuda_fp16.h>

__constant__ float const_diffusion_constants[3*100]; // Assuming a maximum of 1024 timesteps

__global__ void denoise(
    float* model_output, 
    float* sample, 
    long* timestep, 
    float* diffusion_noise,
    float* out
) {
    int tid = threadIdx.x;
    int constants_offset = (*timestep) * 3;

    float weighted_noise = model_output[tid] * const_diffusion_constants[constants_offset];
    float weighted_sample = (sample[tid] - weighted_noise) * const_diffusion_constants[constants_offset + 1];
    weighted_sample = fmax(-1.0, fmin(1.0, weighted_sample));
    weighted_sample += diffusion_noise[tid] * const_diffusion_constants[constants_offset + 2];

    out[tid] = weighted_sample;
}

torch::Tensor denoise_cuda(
    torch::Tensor& model_output,
    torch::Tensor& sample,
    torch::Tensor& diffusion_constants,
    torch::Tensor& timestep,
    torch::Tensor& diffusion_noise
){
    model_output = model_output.contiguous();
    sample = sample.contiguous();
    diffusion_constants = diffusion_constants.contiguous();
    timestep = timestep.contiguous();
    diffusion_noise = diffusion_noise.contiguous();

    float* d_model_output = model_output.data_ptr<float>();
    float* d_sample = sample.data_ptr<float>();
    long* d_timestep = timestep.data_ptr<long>();
    float* d_diffusion_noise = diffusion_noise.data_ptr<float>();
    
    // Copy diffusion constants to constant memory
    cudaMemcpyToSymbol(const_diffusion_constants, diffusion_constants.data_ptr<float>(), diffusion_constants.numel() * sizeof(float));

    auto options = sample.options();
    auto out = torch::empty({1, 2, 16}, options);

    cudaStream_t stream = at::cuda::getCurrentCUDAStream();

    denoise<<<1, 32, 0, stream>>>(d_model_output, d_sample, d_timestep, d_diffusion_noise, out.data_ptr<float>());

    return out;
}