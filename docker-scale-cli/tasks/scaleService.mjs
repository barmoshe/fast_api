// tasks/scaleService.mjs
import inquirer from 'inquirer';
import { scaleService, getCurrentReplicas, displayRunningContainers } from '../utils/dockerHelpers.mjs';
import { handleError } from '../utils/errorHandlers.mjs';

export async function scaleDockerService(action) {
  const serviceName = 'app';

  try {
    const currentReplicas = await getCurrentReplicas(serviceName);
    const { replicas } = await inquirer.prompt([
      {
        type: 'input',
        name: 'replicas',
        message: `Enter the number of replicas to scale ${action === 'up' ? 'to increase' : 'to decrease'}:`,
        validate: (input) => {
          const num = parseInt(input, 10);
          if (isNaN(num) || num < 0) {
            return 'Please enter a valid non-negative number.';
          }
          if (action === 'up' && num <= currentReplicas) {
            return `Number must be greater than current replicas (${currentReplicas}).`;
          }
          if (action === 'down' && num >= currentReplicas) {
            return `Number must be less than current replicas (${currentReplicas}).`;
          }
          return true;
        },
        filter: (input) => parseInt(input, 10),
      },
    ]);

    await scaleService(serviceName, replicas);
    await displayRunningContainers();
  } catch (error) {
    handleError(error);
  }
}
