from redgiant import sensors


def run():
    print("CPU: ", sensors.get_cpu_temperature())
    print("GPU: ", sensors.get_gpu_temperature())


if __name__ == '__main__':
    run()
