import requests
import json
import sys
import argparse
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class MedicalDiagnosisClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        
    def check_server_health(self):
        """Check if the server is running and healthy"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "unhealthy", "error": f"Status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def get_available_models(self):
        """Get information about available prediction models"""
        try:
            response = requests.get(f"{self.server_url}/models", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def open_web_interface(self):
        """Open the web interface in the default browser"""
        webbrowser.open(self.server_url)
        print(f"Opening web interface at {self.server_url}")

class MedicalDiagnosisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Diagnosis System Client")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.client = MedicalDiagnosisClient()
        
        self.create_widgets()
        self.check_server_status()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Server Status", padding="10")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Checking server status...")
        self.status_label.pack(anchor=tk.W)
        
        self.refresh_button = ttk.Button(status_frame, text="Refresh Status", command=self.check_server_status)
        self.refresh_button.pack(anchor=tk.W, pady=(5, 0))
        
        # Available models frame
        models_frame = ttk.LabelFrame(main_frame, text="Available Models", padding="10")
        models_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.models_tree = ttk.Treeview(models_frame, columns=('Status',), show='headings')
        self.models_tree.heading('Status', text='Status')
        self.models_tree.column('Status', width=100, anchor=tk.CENTER)
        self.models_tree.pack(fill=tk.BOTH, expand=True)
        
        # Actions frame
        actions_frame = ttk.Frame(main_frame, padding="10")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.open_web_button = ttk.Button(
            actions_frame, 
            text="Open Web Interface", 
            command=self.open_web_interface
        )
        self.open_web_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.exit_button = ttk.Button(
            actions_frame,
            text="Exit",
            command=self.root.destroy
        )
        self.exit_button.pack(side=tk.RIGHT)
    
    def check_server_status(self):
        """Check and update server status"""
        health_info = self.client.check_server_health()
        
        if health_info.get("status") == "healthy":
            self.status_label.config(
                text=f"Server is running and healthy. Models available: {health_info.get('models_available', 'Unknown')}", 
                foreground="green"
            )
            self.open_web_button.config(state=tk.NORMAL)
            self.update_models_list()
        else:
            error_msg = health_info.get("error", "Unknown error")
            self.status_label.config(
                text=f"Server is not available. Error: {error_msg}", 
                foreground="red"
            )
            self.open_web_button.config(state=tk.DISABLED)
            
            # Clear the models list
            for i in self.models_tree.get_children():
                self.models_tree.delete(i)
    
    def update_models_list(self):
        """Update the list of available models"""
        models_info = self.client.get_available_models()
        
        # Clear existing items
        for i in self.models_tree.get_children():
            self.models_tree.delete(i)
            
        if "error" in models_info:
            messagebox.showerror("Error", f"Failed to get models: {models_info['error']}")
            return
            
        # Add models to the tree
        available_models = models_info.get("available_models", {})
        for disease, available in available_models.items():
            status = "Available" if available else "Not Available"
            status_color = "green" if available else "red"
            
            # Format the disease name
            display_name = disease.replace('_', ' ').title()
            
            # Insert into tree with appropriate color
            item_id = self.models_tree.insert('', tk.END, text=display_name, values=(status,))
            self.models_tree.item(item_id, tags=(status_color,))
            
        # Configure tag colors
        self.models_tree.tag_configure('green', foreground='green')
        self.models_tree.tag_configure('red', foreground='red')
    
    def open_web_interface(self):
        """Open the web interface"""
        self.client.open_web_interface()
        
def main():
    parser = argparse.ArgumentParser(description='Medical Diagnosis System Client')
    parser.add_argument('--server', default='http://localhost:5000', help='Server URL')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    args = parser.parse_args()
    
    client = MedicalDiagnosisClient(server_url=args.server)
    
    # If GUI mode is requested
    if args.gui:
        root = tk.Tk()
        app = MedicalDiagnosisGUI(root)
        root.mainloop()
        return
        
    # Otherwise, use command line interface
    print("\nMedical Diagnosis System Client")
    print("==============================")
    print(f"Server URL: {args.server}")

    # Check server health
    print("\nChecking server health...")
    health_info = client.check_server_health()
    if health_info.get("status") == "healthy":
        print("✓ Server is healthy")
        print(f"  Models available: {health_info.get('models_available', 'Unknown')}")
        
        # Get available models
        print("\nAvailable models:")
        models_info = client.get_available_models()
        if "error" not in models_info:
            available_models = models_info.get("available_models", {})
            for disease, available in available_models.items():
                status = "✓ Available" if available else "✗ Not available"
                print(f"  {disease.capitalize()}: {status}")
        else:
            print(f"  Error fetching models: {models_info.get('error')}")
            
        # Ask to open web interface
        response = input("\nWould you like to open the web interface? (y/n): ")
        if response.lower() in ['y', 'yes']:
            client.open_web_interface()
    else:
        print("✗ Server is not healthy")
        print(f"  Error: {health_info.get('error', 'Unknown error')}")
        print("\nMake sure the server is running and try again.")

if __name__ == "__main__":
    main()
