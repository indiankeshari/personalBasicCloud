import tkinter as tk
from tkinter import filedialog
import boto3
from botocore.exceptions import NoCredentialsError
from tkinter import font


ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

def launch_instance():
    try:
        response = ec2.run_instances(
            ImageId='ami-0c55b159cbfafe1f0',
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        insert_output(f"EC2 Instance Launched: {instance_id}\n")
    except NoCredentialsError:
        insert_output("AWS credentials not available.\n")
    except Exception as e:
        insert_output(f"Error: {str(e)}\n")

def terminate_instance():
    try:
        instance_id = instance_id_entry.get()
        ec2.terminate_instances(InstanceIds=[instance_id])
        insert_output(f"EC2 Instance Terminated: {instance_id}\n")
    except NoCredentialsError:
        insert_output("AWS credentials not available.\n")
    except Exception as e:
        insert_output(f"Error: {str(e)}\n")

def create_bucket():
    try:
        bucket_name = bucket_name_entry.get()
        s3.create_bucket(Bucket=bucket_name)
        insert_output(f"S3 Bucket Created: {bucket_name}\n")
    except NoCredentialsError:
        insert_output("AWS credentials not available.\n")
    except Exception as e:
        insert_output(f"Error: {str(e)}\n")

def upload_file():
    try:
        file_path = filedialog.askopenfilename()
        bucket_name = bucket_name_entry.get()
        s3.upload_file(file_path, bucket_name, file_path.split('/')[-1])
        insert_output(f"File Uploaded: {file_path}\n")
    except NoCredentialsError:
        insert_output("AWS credentials not available.\n")
    except Exception as e:
        insert_output(f"Error: {str(e)}\n")

def delete_file():
    try:
        bucket_name = bucket_name_entry.get()
        file_name = file_name_entry.get()
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        insert_output(f"File Deleted: {file_name}\n")
    except NoCredentialsError:
        insert_output("AWS credentials not available.\n")
    except Exception as e:
        insert_output(f"Error: {str(e)}\n")

def insert_output(message):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message)
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)

root = tk.Tk()
root.title("Personal Cloud Platform")

entry_font = font.Font(size=11)

button_width = 30
button_height = 2

launch_button = tk.Button(root, text="Launch EC2 Instance", command=launch_instance, width=button_width, height=button_height)
terminate_button = tk.Button(root, text="Terminate EC2 Instance", command=terminate_instance, width=button_width, height=button_height)
create_bucket_button = tk.Button(root, text="Create S3 Bucket", command=create_bucket, width=button_width, height=button_height)
upload_button = tk.Button(root, text="Upload to S3 Bucket", command=upload_file, width=button_width, height=button_height)
delete_button = tk.Button(root, text="Delete from S3 Bucket", command=delete_file, width=button_width, height=button_height)

entry_width = 27

instance_id_entry = tk.Entry(root, width=entry_width, font=entry_font)
instance_id_entry.insert(0, "Enter Instance ID")

bucket_name_entry = tk.Entry(root, width=entry_width, font=entry_font)
bucket_name_entry.insert(0, "Enter Bucket Name")

file_name_entry = tk.Entry(root, width=entry_width, font=entry_font)
file_name_entry.insert(0, "Enter File Name")

output_text = tk.Text(root, height=10, width=60, wrap=tk.WORD, padx=5, pady=5)
output_text.config(state=tk.DISABLED)

launch_button.pack(pady=5)
terminate_button.pack(pady=5)
instance_id_entry.pack(pady=5)
create_bucket_button.pack(pady=5)
bucket_name_entry.pack(pady=5)
upload_button.pack(pady=5)
delete_button.pack(pady=5)
file_name_entry.pack(pady=5)
output_text.pack(pady=20)

root.mainloop()
