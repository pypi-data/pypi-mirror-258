#include <ATen/ATen.h>
#include <torch/extension.h>
#include <vector>

torch::Tensor denoise_cuda(
    torch::Tensor& model_output,
    torch::Tensor& sample,
    torch::Tensor& diffusion_constants,
    torch::Tensor& timestep,
    torch::Tensor& diffusion_noise
);

torch::Tensor denoise_cuda_wrapper(
    torch::Tensor& model_output,
    torch::Tensor& sample,
    torch::Tensor& diffusion_constants,
    torch::Tensor& timestep,
    torch::Tensor& diffusion_noise)
{
    at::DeviceGuard guard(model_output.device());
    return denoise_cuda(model_output, sample, diffusion_constants, timestep, diffusion_noise);
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("denoise", &denoise_cuda_wrapper, "Denoise wrapper function",
          py::arg("model_output"), py::arg("sample"), py::arg("diffusion_constants"), py::arg("timestep"), py::arg("diffusion_noise"));
}
