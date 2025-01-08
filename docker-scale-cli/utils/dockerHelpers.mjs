// utils/dockerHelpers.mjs
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function checkDockerComposeInstalled() {
  try {
    await execAsync('docker-compose --version');
  } catch (error) {
    throw new Error('docker-compose is not installed. Please install it first.');
  }
}

export async function getCurrentReplicas(serviceName) {
  try {
    const { stdout } = await execAsync(`docker-compose ps -q ${serviceName}`);
    const containerIds = stdout.trim().split('\n').filter(id => id);
    return containerIds.length;
  } catch (error) {
    throw new Error(`Failed to get current replicas: ${error.message}`);
  }
}

export async function scaleService(serviceName, replicas) {
  try {
    console.log(`\nScaling the '${serviceName}' service to ${replicas} replicas...`);
    const { stdout, stderr } = await execAsync(`docker-compose up -d --scale ${serviceName}=${replicas} --no-recreate`);


    console.log(stdout);

    const newReplicas = await getCurrentReplicas(serviceName);
    if (newReplicas === replicas) {
      console.log(`Successfully scaled the '${serviceName}' service to ${replicas} replicas.`);
    } else {
      console.warn(`Desired replicas: ${replicas}, but found: ${newReplicas}. Please check the Docker Compose setup.`);
    }
  } catch (error) {

    throw new Error(`Failed to scale the '${serviceName}' service: ${error.message}`);
  }
}

export async function displayRunningContainers() {
  try {
    const { stdout } = await execAsync('docker ps');
    console.log('\nCurrently running containers:');
    console.log(stdout);
  } catch (error) {
    throw new Error(`Failed to retrieve running containers: ${error.message}`);
  }
}


export async function reloadNginx() {
  console.log('\nReloading Nginx to update upstream servers...');
  try {
    const { stdout, stderr } = await execAsync(`docker-compose exec nginx nginx -s reload`);

    // Optionally log stderr as a warning without throwing an error
    if (stderr && stderr.trim() !== '') {
      console.warn(`Nginx stderr: ${stderr.trim()}`);
    }

    console.log(stdout);
    console.log('Nginx reloaded successfully.');
  } catch (error) {
    throw new Error(`Failed to reload Nginx: ${error.message}`);
  }
}