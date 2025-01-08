// mainMenu.mjs
import inquirer from 'inquirer';
import { choices } from './constants.mjs';
import { scaleDockerService } from './tasks/scaleService.mjs';
import { handleError } from './utils/errorHandlers.mjs';
import { checkDockerComposeInstalled, getCurrentReplicas } from './utils/dockerHelpers.mjs';

export async function mainMenu() {
  const serviceName = 'app';
  try {
    await checkDockerComposeInstalled();
    const currentReplicas = await getCurrentReplicas(serviceName);
        console.log(`
    Current number of replicas for '${serviceName}': ${currentReplicas}`);
    

    const answer = await inquirer.prompt([
      {
        type: 'list',
        name: 'task',
        message: 'Select a task to perform:',
        choices: choices,
      },
    ]);

    switch (answer.task) {
      case choices[0]:
        await scaleDockerService('up');
        break;
      case choices[1]:
        await scaleDockerService('down');
        break;
      default:
        console.log('Exiting...');
        process.exit(0);
    }

    await mainMenu();
  } catch (error) {
    handleError(error);
    await mainMenu();
  }
}

mainMenu();
