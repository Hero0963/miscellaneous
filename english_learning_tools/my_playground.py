import torch


def _simple_run():
    print("hello, world")


def test_cuda():
    if torch.cuda.is_available():
        print("CUDA is available!")
        print(f"Number of CUDA devices: {torch.cuda.device_count()}")
        print(f"CUDA device name: {torch.cuda.get_device_name(0)}")

        # Test creating a tensor on CUDA
        x = torch.tensor([1.0, 2.0, 3.0], device='cuda')
        print(f"Tensor on CUDA: {x}")
    else:
        print("CUDA is not available. Please check your installation.")


if __name__ == '__main__':
    test_cuda()
