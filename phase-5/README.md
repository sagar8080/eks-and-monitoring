### **Prerequisites**
- AWS CLI configured with appropriate credentials.
- `kubectl` and `eksctl` installed and working.
- `Helm` installed for managing Kubernetes applications.
- An SNS topic and email subscription created in AWS.

---

### **Commands Used**

#### **1. Set Up an EKS Cluster**
- Create an EKS cluster using `eksctl`:
  ```bash
  eksctl create cluster --name prometheus-cluster --region us-east-1 --nodes 2 --node-type t3.medium
  ```
- Verify the cluster setup:
  ```bash
  kubectl get nodes
  ```

---

#### **2. Install Prometheus Using Helm**
- Add the Prometheus Helm chart repository:
  ```bash
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  ```
- Install Prometheus using the `kube-prometheus-stack` chart:
  ```bash
  helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
  ```
- Check the status of all resources:
  ```bash
  kubectl get all -n monitoring
  ```

#### **3. Resolve Persistent Volume Issues**
- If PVCs are stuck in `Pending` state, delete and recreate StatefulSets and PVCs:
  ```bash
  kubectl delete pvc prometheus-server -n monitoring
  kubectl delete statefulset prometheus-server -n monitoring
  ```
- Reinstall Prometheus with updated storage configurations: `Note`: The values.yaml contain the alert configuration so we do not have to explicitly define them in the alerting-rules.yaml
  ```bash
  helm upgrade --install prometheus prometheus-community/prometheus -n monitoring -f values.yaml
  ```

---

#### **4. Test Alerting Rules**
- Create a test pod that restarts every 5 minutes:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-pod
    namespace: default
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: test-pod
    template:
      metadata:
        labels:
          app: test-pod
      spec:
        containers:
        - name: test-container
          image: busybox
          args:
          - /bin/sh
          - -c
          - |
            echo "This pod will restart every 5 minutes.";
            sleep 300;
            exit 1;
  ```
- Apply the test pod:
  ```bash
  kubectl apply -f test-pod.yaml
  ```
- Monitor the restart counts using the Prometheus dashboard.

---

#### **5. Integrate AlertManager with AWS SNS**
- Update the `alertmanager.yml` configuration to include a webhook pointing to an API Gateway:
  ```yaml
  global:
    resolve_timeout: 5m
  route:
    receiver: sns
  receivers:
    - name: sns
      webhook_configs:
      - url: https://<api-gateway-id>.execute-api.<region>.amazonaws.com/prod
        send_resolved: true
  ```
- Reload AlertManager configuration:
  ```bash
  kubectl exec -n monitoring <alertmanager-pod> -- curl -X POST http://localhost:9093/-/reload
  ```

---

#### **6. Test SNS Integration**
- Simulate an alert by increasing the pod restart count.
- Verify logs to ensure the webhook is triggered:
  ```bash
  kubectl logs -l app.kubernetes.io/name=alertmanager -n monitoring
  ```
- Confirm receipt of an email notification from SNS.

---

### **Cleanup Commands**
To clean up the Prometheus setup:
1. Scale down StatefulSets and Deployments:
   ```bash
   kubectl scale statefulset --all --replicas=0 -n monitoring
   kubectl scale deployment --all --replicas=0 -n monitoring
   ```
2. Delete all resources in the `monitoring` namespace:
   ```bash
   kubectl delete all --all -n monitoring
   kubectl delete pvc --all -n monitoring
   ```
3. Delete the `monitoring` namespace:
   ```bash
   kubectl delete namespace monitoring
   ```
4. Delete the EKS cluster:
   ```bash
   eksctl delete cluster --name prometheus-cluster --region us-east-1
   ```
