
import os
import grpc
import numpy as np
import tensorflow as tf
import predict_pb2
import predict_pb2_grpc
from concurrent import futures

# File name for the trained model
MODEL_PATH = "train_investpro_ai_dnn_model.h5"


class PredictorService(predict_pb2_grpc.PredictorServicer):
    def __init__(self, model_path="train_investpro_ai_dnn_model.h5"):
        if not os.path.exists(model_path):
            print("⚠️ Model not found. Creating a dummy model with random weights...")
            model = tf.keras.Sequential(
                [
                    tf.keras.layers.Input(shape=(11,)),
                    tf.keras.layers.Dense(64, activation="relu"),
                    tf.keras.layers.Dense(1, activation="sigmoid"),
                ]
            )
            model.compile(optimizer="adam", loss="binary_crossentropy")
            dummy_data = np.random.rand(100, 11)
            dummy_labels = np.random.randint(0, 2, size=(100,))
            model.fit(dummy_data, dummy_labels, epochs=1, verbose=0)
            model.save(model_path)

        self.model = tf.keras.models.load_model(model_path)
        if self.model.input_shape[-1] != 11:
            raise ValueError(
                f"Expected model input shape with 11 features, got {self.model.input_shape[-1]}"
            )

    def Predict(self, request, context):
        features = np.array(
            [
                [
                    request.open,
                    request.close,
                    request.high,
                    request.low,
                    request.volume,
                    request.rsi,
                    request.atr,
                    request.macd,
                    request.stoch,
                    request.bb_upper,
                    request.bb_lower,
                ]
            ],
            dtype=np.float32,
        )

        prediction = self.model.predict(features, verbose=0)
        confidence = float(prediction[0][0])
        label = "up" if confidence > 0.5 else "down"

        return predict_pb2.PredictionResponse(prediction=label, confidence=confidence)


    
    def HealthCheck(self, request, context):
     print("✅ HealthCheck received from client.")
     return predict_pb2.HealthStatus(status="SERVING")



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    predict_pb2_grpc.add_PredictorServicer_to_server(PredictorService(), server)
    server.add_insecure_port("[::]:50051")
    print("✅ AI Prediction Server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

