# Distributed File System Project

## Project Overview
This project is a distributed file system designed to efficiently manage files across multiple nodes. Each node is composed of two simultaneously running programs:

1. **Name Server**:
   - Acts as a central coordinator for the distributed network.
   - Facilitates communication between nodes by managing file metadata, such as locations and access permissions.
   - Routes requests for file transfer, ensuring the correct nodes are engaged for uploading, downloading, or modifying files.

2. **Dockerized Flask Application**:
   - Provides a user-friendly interface to locally manage files on each node through a web browser.
   - Includes functionalities such as uploading, downloading, renaming, and deleting files.
   - Encapsulated in a Docker container alongside the node's local file storage, simplifying deployment and ensuring consistency across environments.

## Key Features
- **Distributed Architecture**: Files and metadata are spread across multiple nodes, improving fault tolerance and scalability.
- **Centralized Coordination**: The name server ensures efficient communication and prevents conflicts in the distributed environment.
- **Web-Based Management**: The Flask application allows for intuitive file management, accessible through any modern browser.
- **Containerization**: Docker simplifies deployment, enabling consistent and isolated environments for each node.

### Prerequisites
- Docker and Docker Compose installed on your system.
- Python 3.8+ installed locally for development purposes (optional).
- Network setup to ensure nodes can communicate with each other.



