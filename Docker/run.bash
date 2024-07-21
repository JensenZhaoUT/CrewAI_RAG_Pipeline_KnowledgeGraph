xhost local:root
XAUTH=/tmp/.docker.xauth
docker run --rm -it \
    --name=rag_container\
    --volume="/home/$USER//projects/Agentic_RAG_Pipeline_KnowledgeGraph:/app" \
    --volume="/dev/bus/usb:/dev/bus/usb" \
    --volume="/tmp/.docker.xauth:/tmp/.docker.xauth:rw" \
    --gpus=all \
    --net=host \
    --privileged \
    rag-pipeline \
    bash

echo "Done."