import time

class ModelMeter:
    def __init__(self, model):
        self.model = model

    def measure(self, image, min_iterations=10, max_duration=30):

        # warmup
        self.model(image)

        start_time = time.time()
        iterations = 0
        while True:
            self.model(image)
            iterations += 1
            current_time = time.time()
            if iterations >= min_iterations and (current_time - start_time) > max_duration:
                break

        total_time = current_time - start_time
        throughput = iterations / total_time
        avg_time_per_image = total_time / iterations

        print(f"Throughput: {throughput:.2f} images/second")
        print(f"Average time per image: {avg_time_per_image:.4f} seconds")

        return throughput, avg_time_per_image
