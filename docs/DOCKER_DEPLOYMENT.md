# Practical 10: Containerization of ML Application Using Docker

## 1. Objective

To containerize the Iris Machine Learning application using Docker, package the trained model and dependencies, build a Docker image, and deploy the application inside a running container.

## 2. Tools and Technologies

- Python 3.11
- Docker Desktop
- Docker Engine
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Git and GitHub

## 3. Project Components

- `Dockerfile` - Defines the multi-stage Docker image.
- `.dockerignore` - Excludes unnecessary files from the build context.
- `requirements-serving.txt` - Contains serving dependencies.
- `src/train_final_model.py` - Trains and saves the Random Forest model.
- `src/serve.py` - Provides HTTP health and prediction endpoints.
- `data/processed/iris_features.csv` - Processed Iris dataset.

## 4. Docker Architecture

The Dockerfile uses a multi-stage build.

### Builder Stage

- Uses Python 3.11 slim.
- Installs required dependencies.
- Copies the processed Iris dataset.
- Trains the Random Forest classifier.
- Saves the trained model and label encoder.

### Runtime Stage

- Uses Python 3.11 slim.
- Copies the required dependencies.
- Copies the trained model and label encoder.
- Copies the prediction server.
- Exposes port 8000.
- Configures a Docker health check.

This approach keeps training files and the dataset out of the final runtime image.

## 5. Docker Image Creation

Command:

```bash
docker build -t iris-classifier:v1 .
```

Result:

- Image created successfully.
- Image name: `iris-classifier`
- Tag: `v1`
- Image ID: `8d36d4082365`
- Disk usage: 680 MB
- Content size: 155 MB

## 6. Container Deployment

Command:

```bash
docker run -d --name iris-classifier-container -p 8000:8000 iris-classifier:v1
```

The container started successfully.

- Container name: `iris-classifier-container`
- Port mapping: 8000:8000
- Status: Running and healthy

## 7. Application Testing

### A. Health Check

Request:

```bash
curl http://localhost:8000/health
```

Response:

```json
{"status": "healthy"}
```

Result: Successful.

### B. Iris Prediction

Endpoint:

`POST http://localhost:8000/predict`

Sample input:

- Sepal length: 5.1
- Sepal width: 3.5
- Petal length: 1.4
- Petal width: 0.2
- Sepal area: 17.85
- Petal area: 0.28
- Sepal-to-petal length ratio: 3.642857

Actual response:

```json
{
  "prediction": "setosa",
  "probabilities": [1.0, 0.0, 0.0]
}
```

Result: Successful prediction.

### C. Invalid Input Testing

An incomplete JSON request was submitted.

Actual result:

- HTTP Status: 400 Bad Request
- Error: Missing features

Result: Input validation working correctly.

## 8. Docker Health Monitoring

Command:

```bash
docker inspect --format='{{.State.Health.Status}}' iris-classifier-container
```

Observed result:

`healthy`

The Docker health check successfully monitored the application.

## 9. Docker Image Inspection

Commands:

```bash
docker images iris-classifier
docker history iris-classifier:v1
docker logs iris-classifier-container
```

The image layers, image size, and application logs were inspected successfully.

## 10. Docker Layer Caching

The Docker image was built again using the same command.

- First build time: 115.5 seconds
- Second build time: 3.1 seconds

Result: Docker reused cached layers, reducing rebuild time significantly.

## 11. Multi-stage Build Advantages

- Separates model training from application serving.
- Keeps the dataset and training script out of the runtime stage.
- Improves build organization.
- Supports dependency and layer caching.
- Makes deployment more efficient.

A separate single-stage image was not built, so no measured image-size comparison is reported.

## 12. Cleanup

The previous test container was stopped and removed successfully.

Commands:

```bash
docker stop iris-classifier-container
docker rm iris-classifier-container
```

The Docker image was preserved.

A fresh container was subsequently started and verified as healthy.

## 13. Conclusion

The Iris Machine Learning application was successfully containerized using Docker.

A multi-stage Dockerfile was created to train the model and prepare a separate runtime environment. The Docker image was built, the application was deployed, and both health and prediction endpoints were tested successfully.

Docker image caching was also verified by rebuilding the image. This practical demonstrated how Docker simplifies the packaging and deployment of Machine Learning applications.