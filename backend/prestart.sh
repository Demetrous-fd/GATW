#! /usr/bin/env sh

echo "Waiting for services to start for 30 seconds"
sleep 30

echo "Create access_key and secret_key for minio"
./mc config host add myminio http://${MINIO_HOST}:${MINIO_API_PORT} ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
./mc admin user add myminio ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}
./mc admin policy set myminio readwrite user=${MINIO_ACCESS_KEY}

echo "Run migration"
alembic upgrade b91b0987b75d
alembic upgrade head