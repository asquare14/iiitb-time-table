if [ "$TRAVIS_BRANCH" = "develop" ]; then
TAG="latest"
else
TAG="$TRAVIS_BRANCH"
fi
docker build -f Dockerfile -t "asquare14/whats-slot-iiitb":$TAG .
docker login --username=$DOCKER_USER --password=$DOCKER_PASS
docker push asquare14/whats-slot-iiitb:$TAG