# Use the official OpenJDK 17 image from public.ecr.aws, since Docker Hub has some rate limits
FROM public.ecr.aws/amazoncorretto/amazoncorretto:17.0.13-al2-native-jdk
# Set working directory inside the container
WORKDIR /app
# Copy the compiled Java application JAR file into the container
COPY ./target/learn4lombok /app
# Expose the port the Spring Boot application will run on
EXPOSE 8080
EXPOSE 80
# Command to run the application
CMD ["java", "-jar", "learn4lombok.jar"]
