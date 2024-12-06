You can either delete the namespace or use manual deletion

### Delete the namespace:
   ```bash
   kubectl delete namespace otel-demo
   ```

### Verify that the namespace and its resources are removed:
   ```bash
   kubectl get namespaces
   ```
### Delete Manually

1. **Delete Deployments:**
   ```bash
   kubectl delete deployments --all -n otel-demo
   ```

2. **Delete Services:**
   ```bash
   kubectl delete services --all -n otel-demo
   ```

3. **Delete Pods:**
   ```bash
   kubectl delete pods --all -n otel-demo
   ```

4. **Delete ConfigMaps and Other Resources:**
   ```bash
   kubectl delete configmaps --all -n otel-demo
   kubectl delete secrets --all -n otel-demo
   kubectl delete persistentvolumeclaims --all -n otel-demo
   ```

5. Verify that the namespace is clean:
   ```bash
   kubectl get all -n otel-demo
   ```
   
### Copy the split YAML
```
scp -i "key.pem" -r <path-to-split-yaml> ec2-user@<public-ip>:/home/ec2-user/split_yaml
```

### Recreate the Namespace
Recreate the `otel-demo` namespace:
```bash
kubectl create namespace otel-demo
```

### Reapply the YAML Files
Reapply the split YAML files to the recreated namespace:
1. Navigate to the directory containing the split YAML files:
   ```bash
   cd split_yaml
   ```

2. Apply all files recursively:
   ```bash
   kubectl apply -f . --recursive -n otel-demo
   ```

### Verify Deployment
Check the status of the resources in the `otel-demo` namespace:
```bash
kubectl get all -n otel-demo
```

For troubleshooting:
  ```bash
  kubectl describe pod <pod-name> -n otel-demo
  ```
  ```bash
  kubectl logs <pod-name> -n otel-demo
  ```

### Access the Application
Once everything is running:
1. **Port Forwarding**:
   ```bash
   kubectl port-forward -n otel-demo svc/opentelemetry-demo-frontendproxy 8080 
   ```
   Access the application using `ssh -i securekey.pem -L 8080:localhost:8080 ec2-user@<public-ip>`