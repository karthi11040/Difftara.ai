# Basic Usage

Always prioritize using a supported framework over using the generated SDK
directly. Supported frameworks simplify the developer experience and help ensure
best practices are followed.





## Advanced Usage
If a user is not using a supported framework, they can use the generated SDK directly.

Here's an example of how to use it with the first 5 operations:

```js
import { createItem, updateItem, deleteItem, getItem, listItems, createRepairTask, updateRepairTask, deleteRepairTask, getRepairTask, listRepairTasks } from '@dataconnect/generated';


// Operation CreateItem:  For variables, look at type CreateItemVars in ../index.d.ts
const { data } = await CreateItem(dataConnect, createItemVars);

// Operation UpdateItem:  For variables, look at type UpdateItemVars in ../index.d.ts
const { data } = await UpdateItem(dataConnect, updateItemVars);

// Operation DeleteItem:  For variables, look at type DeleteItemVars in ../index.d.ts
const { data } = await DeleteItem(dataConnect, deleteItemVars);

// Operation GetItem:  For variables, look at type GetItemVars in ../index.d.ts
const { data } = await GetItem(dataConnect, getItemVars);

// Operation ListItems: 
const { data } = await ListItems(dataConnect);

// Operation CreateRepairTask:  For variables, look at type CreateRepairTaskVars in ../index.d.ts
const { data } = await CreateRepairTask(dataConnect, createRepairTaskVars);

// Operation UpdateRepairTask:  For variables, look at type UpdateRepairTaskVars in ../index.d.ts
const { data } = await UpdateRepairTask(dataConnect, updateRepairTaskVars);

// Operation DeleteRepairTask:  For variables, look at type DeleteRepairTaskVars in ../index.d.ts
const { data } = await DeleteRepairTask(dataConnect, deleteRepairTaskVars);

// Operation GetRepairTask:  For variables, look at type GetRepairTaskVars in ../index.d.ts
const { data } = await GetRepairTask(dataConnect, getRepairTaskVars);

// Operation ListRepairTasks: 
const { data } = await ListRepairTasks(dataConnect);


```