# Generated TypeScript README
This README will guide you through the process of using the generated JavaScript SDK package for the connector `example`. It will also provide examples on how to use your generated SDK to call your Data Connect queries and mutations.

***NOTE:** This README is generated alongside the generated SDK. If you make changes to this file, they will be overwritten when the SDK is regenerated.*

# Table of Contents
- [**Overview**](#generated-javascript-readme)
- [**Accessing the connector**](#accessing-the-connector)
  - [*Connecting to the local Emulator*](#connecting-to-the-local-emulator)
- [**Queries**](#queries)
  - [*GetItem*](#getitem)
  - [*ListItems*](#listitems)
  - [*GetRepairTask*](#getrepairtask)
  - [*ListRepairTasks*](#listrepairtasks)
  - [*GetTechnician*](#gettechnician)
  - [*ListTechnicians*](#listtechnicians)
  - [*GetAssignment*](#getassignment)
  - [*ListAssignments*](#listassignments)
  - [*GetShipment*](#getshipment)
  - [*ListShipments*](#listshipments)
- [**Mutations**](#mutations)
  - [*CreateItem*](#createitem)
  - [*UpdateItem*](#updateitem)
  - [*DeleteItem*](#deleteitem)
  - [*CreateRepairTask*](#createrepairtask)
  - [*UpdateRepairTask*](#updaterepairtask)
  - [*DeleteRepairTask*](#deleterepairtask)
  - [*CreateTechnician*](#createtechnician)
  - [*UpdateTechnician*](#updatetechnician)
  - [*DeleteTechnician*](#deletetechnician)
  - [*CreateAssignment*](#createassignment)
  - [*UpdateAssignment*](#updateassignment)
  - [*DeleteAssignment*](#deleteassignment)
  - [*CreateShipment*](#createshipment)
  - [*UpdateShipment*](#updateshipment)
  - [*DeleteShipment*](#deleteshipment)

# Accessing the connector
A connector is a collection of Queries and Mutations. One SDK is generated for each connector - this SDK is generated for the connector `example`. You can find more information about connectors in the [Data Connect documentation](https://firebase.google.com/docs/data-connect#how-does).

You can use this generated SDK by importing from the package `@dataconnect/generated` as shown below. Both CommonJS and ESM imports are supported.

You can also follow the instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#set-client).

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
```

## Connecting to the local Emulator
By default, the connector will connect to the production service.

To connect to the emulator, you can use the following code.
You can also follow the emulator instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#instrument-clients).

```typescript
import { connectDataConnectEmulator, getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
connectDataConnectEmulator(dataConnect, 'localhost', 9399);
```

After it's initialized, you can call your Data Connect [queries](#queries) and [mutations](#mutations) from your generated SDK.

# Queries

There are two ways to execute a Data Connect Query using the generated Web SDK:
- Using a Query Reference function, which returns a `QueryRef`
  - The `QueryRef` can be used as an argument to `executeQuery()`, which will execute the Query and return a `QueryPromise`
- Using an action shortcut function, which returns a `QueryPromise`
  - Calling the action shortcut function will execute the Query and return a `QueryPromise`

The following is true for both the action shortcut function and the `QueryRef` function:
- The `QueryPromise` returned will resolve to the result of the Query once it has finished executing
- If the Query accepts arguments, both the action shortcut function and the `QueryRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Query
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each query. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-queries).

## GetItem
You can execute the `GetItem` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getItem(vars: GetItemVariables, options?: ExecuteQueryOptions): QueryPromise<GetItemData, GetItemVariables>;

interface GetItemRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetItemVariables): QueryRef<GetItemData, GetItemVariables>;
}
export const getItemRef: GetItemRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getItem(dc: DataConnect, vars: GetItemVariables, options?: ExecuteQueryOptions): QueryPromise<GetItemData, GetItemVariables>;

interface GetItemRef {
  ...
  (dc: DataConnect, vars: GetItemVariables): QueryRef<GetItemData, GetItemVariables>;
}
export const getItemRef: GetItemRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getItemRef:
```typescript
const name = getItemRef.operationName;
console.log(name);
```

### Variables
The `GetItem` query requires an argument of type `GetItemVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetItemVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetItem` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetItemData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetItemData {
  item?: {
    name: string;
    status: string;
  };
}
```
### Using `GetItem`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getItem, GetItemVariables } from '@dataconnect/generated';

// The `GetItem` query requires an argument of type `GetItemVariables`:
const getItemVars: GetItemVariables = {
  id: ..., 
};

// Call the `getItem()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getItem(getItemVars);
// Variables can be defined inline as well.
const { data } = await getItem({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getItem(dataConnect, getItemVars);

console.log(data.item);

// Or, you can use the `Promise` API.
getItem(getItemVars).then((response) => {
  const data = response.data;
  console.log(data.item);
});
```

### Using `GetItem`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getItemRef, GetItemVariables } from '@dataconnect/generated';

// The `GetItem` query requires an argument of type `GetItemVariables`:
const getItemVars: GetItemVariables = {
  id: ..., 
};

// Call the `getItemRef()` function to get a reference to the query.
const ref = getItemRef(getItemVars);
// Variables can be defined inline as well.
const ref = getItemRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getItemRef(dataConnect, getItemVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.item);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.item);
});
```

## ListItems
You can execute the `ListItems` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listItems(options?: ExecuteQueryOptions): QueryPromise<ListItemsData, undefined>;

interface ListItemsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListItemsData, undefined>;
}
export const listItemsRef: ListItemsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listItems(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListItemsData, undefined>;

interface ListItemsRef {
  ...
  (dc: DataConnect): QueryRef<ListItemsData, undefined>;
}
export const listItemsRef: ListItemsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listItemsRef:
```typescript
const name = listItemsRef.operationName;
console.log(name);
```

### Variables
The `ListItems` query has no variables.
### Return Type
Recall that executing the `ListItems` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListItemsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListItemsData {
  items: ({
    id: UUIDString;
    name: string;
    status: string;
  } & Item_Key)[];
}
```
### Using `ListItems`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listItems } from '@dataconnect/generated';


// Call the `listItems()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listItems();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listItems(dataConnect);

console.log(data.items);

// Or, you can use the `Promise` API.
listItems().then((response) => {
  const data = response.data;
  console.log(data.items);
});
```

### Using `ListItems`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listItemsRef } from '@dataconnect/generated';


// Call the `listItemsRef()` function to get a reference to the query.
const ref = listItemsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listItemsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.items);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.items);
});
```

## GetRepairTask
You can execute the `GetRepairTask` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getRepairTask(vars: GetRepairTaskVariables, options?: ExecuteQueryOptions): QueryPromise<GetRepairTaskData, GetRepairTaskVariables>;

interface GetRepairTaskRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetRepairTaskVariables): QueryRef<GetRepairTaskData, GetRepairTaskVariables>;
}
export const getRepairTaskRef: GetRepairTaskRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getRepairTask(dc: DataConnect, vars: GetRepairTaskVariables, options?: ExecuteQueryOptions): QueryPromise<GetRepairTaskData, GetRepairTaskVariables>;

interface GetRepairTaskRef {
  ...
  (dc: DataConnect, vars: GetRepairTaskVariables): QueryRef<GetRepairTaskData, GetRepairTaskVariables>;
}
export const getRepairTaskRef: GetRepairTaskRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getRepairTaskRef:
```typescript
const name = getRepairTaskRef.operationName;
console.log(name);
```

### Variables
The `GetRepairTask` query requires an argument of type `GetRepairTaskVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetRepairTaskVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetRepairTask` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetRepairTaskData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetRepairTaskData {
  repairTask?: {
    startDate: TimestampString;
    status: string;
    item: {
      name: string;
    };
  };
}
```
### Using `GetRepairTask`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getRepairTask, GetRepairTaskVariables } from '@dataconnect/generated';

// The `GetRepairTask` query requires an argument of type `GetRepairTaskVariables`:
const getRepairTaskVars: GetRepairTaskVariables = {
  id: ..., 
};

// Call the `getRepairTask()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getRepairTask(getRepairTaskVars);
// Variables can be defined inline as well.
const { data } = await getRepairTask({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getRepairTask(dataConnect, getRepairTaskVars);

console.log(data.repairTask);

// Or, you can use the `Promise` API.
getRepairTask(getRepairTaskVars).then((response) => {
  const data = response.data;
  console.log(data.repairTask);
});
```

### Using `GetRepairTask`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getRepairTaskRef, GetRepairTaskVariables } from '@dataconnect/generated';

// The `GetRepairTask` query requires an argument of type `GetRepairTaskVariables`:
const getRepairTaskVars: GetRepairTaskVariables = {
  id: ..., 
};

// Call the `getRepairTaskRef()` function to get a reference to the query.
const ref = getRepairTaskRef(getRepairTaskVars);
// Variables can be defined inline as well.
const ref = getRepairTaskRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getRepairTaskRef(dataConnect, getRepairTaskVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.repairTask);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.repairTask);
});
```

## ListRepairTasks
You can execute the `ListRepairTasks` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listRepairTasks(options?: ExecuteQueryOptions): QueryPromise<ListRepairTasksData, undefined>;

interface ListRepairTasksRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListRepairTasksData, undefined>;
}
export const listRepairTasksRef: ListRepairTasksRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listRepairTasks(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListRepairTasksData, undefined>;

interface ListRepairTasksRef {
  ...
  (dc: DataConnect): QueryRef<ListRepairTasksData, undefined>;
}
export const listRepairTasksRef: ListRepairTasksRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listRepairTasksRef:
```typescript
const name = listRepairTasksRef.operationName;
console.log(name);
```

### Variables
The `ListRepairTasks` query has no variables.
### Return Type
Recall that executing the `ListRepairTasks` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListRepairTasksData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListRepairTasksData {
  repairTasks: ({
    id: UUIDString;
    startDate: TimestampString;
    status: string;
  } & RepairTask_Key)[];
}
```
### Using `ListRepairTasks`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listRepairTasks } from '@dataconnect/generated';


// Call the `listRepairTasks()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listRepairTasks();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listRepairTasks(dataConnect);

console.log(data.repairTasks);

// Or, you can use the `Promise` API.
listRepairTasks().then((response) => {
  const data = response.data;
  console.log(data.repairTasks);
});
```

### Using `ListRepairTasks`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listRepairTasksRef } from '@dataconnect/generated';


// Call the `listRepairTasksRef()` function to get a reference to the query.
const ref = listRepairTasksRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listRepairTasksRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.repairTasks);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.repairTasks);
});
```

## GetTechnician
You can execute the `GetTechnician` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getTechnician(vars: GetTechnicianVariables, options?: ExecuteQueryOptions): QueryPromise<GetTechnicianData, GetTechnicianVariables>;

interface GetTechnicianRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetTechnicianVariables): QueryRef<GetTechnicianData, GetTechnicianVariables>;
}
export const getTechnicianRef: GetTechnicianRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getTechnician(dc: DataConnect, vars: GetTechnicianVariables, options?: ExecuteQueryOptions): QueryPromise<GetTechnicianData, GetTechnicianVariables>;

interface GetTechnicianRef {
  ...
  (dc: DataConnect, vars: GetTechnicianVariables): QueryRef<GetTechnicianData, GetTechnicianVariables>;
}
export const getTechnicianRef: GetTechnicianRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getTechnicianRef:
```typescript
const name = getTechnicianRef.operationName;
console.log(name);
```

### Variables
The `GetTechnician` query requires an argument of type `GetTechnicianVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetTechnicianVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetTechnician` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetTechnicianData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetTechnicianData {
  technician?: {
    name: string;
    email: string;
    specialty?: string | null;
  };
}
```
### Using `GetTechnician`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getTechnician, GetTechnicianVariables } from '@dataconnect/generated';

// The `GetTechnician` query requires an argument of type `GetTechnicianVariables`:
const getTechnicianVars: GetTechnicianVariables = {
  id: ..., 
};

// Call the `getTechnician()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getTechnician(getTechnicianVars);
// Variables can be defined inline as well.
const { data } = await getTechnician({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getTechnician(dataConnect, getTechnicianVars);

console.log(data.technician);

// Or, you can use the `Promise` API.
getTechnician(getTechnicianVars).then((response) => {
  const data = response.data;
  console.log(data.technician);
});
```

### Using `GetTechnician`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getTechnicianRef, GetTechnicianVariables } from '@dataconnect/generated';

// The `GetTechnician` query requires an argument of type `GetTechnicianVariables`:
const getTechnicianVars: GetTechnicianVariables = {
  id: ..., 
};

// Call the `getTechnicianRef()` function to get a reference to the query.
const ref = getTechnicianRef(getTechnicianVars);
// Variables can be defined inline as well.
const ref = getTechnicianRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getTechnicianRef(dataConnect, getTechnicianVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.technician);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.technician);
});
```

## ListTechnicians
You can execute the `ListTechnicians` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listTechnicians(options?: ExecuteQueryOptions): QueryPromise<ListTechniciansData, undefined>;

interface ListTechniciansRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListTechniciansData, undefined>;
}
export const listTechniciansRef: ListTechniciansRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listTechnicians(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListTechniciansData, undefined>;

interface ListTechniciansRef {
  ...
  (dc: DataConnect): QueryRef<ListTechniciansData, undefined>;
}
export const listTechniciansRef: ListTechniciansRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listTechniciansRef:
```typescript
const name = listTechniciansRef.operationName;
console.log(name);
```

### Variables
The `ListTechnicians` query has no variables.
### Return Type
Recall that executing the `ListTechnicians` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListTechniciansData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListTechniciansData {
  technicians: ({
    id: UUIDString;
    name: string;
  } & Technician_Key)[];
}
```
### Using `ListTechnicians`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listTechnicians } from '@dataconnect/generated';


// Call the `listTechnicians()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listTechnicians();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listTechnicians(dataConnect);

console.log(data.technicians);

// Or, you can use the `Promise` API.
listTechnicians().then((response) => {
  const data = response.data;
  console.log(data.technicians);
});
```

### Using `ListTechnicians`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listTechniciansRef } from '@dataconnect/generated';


// Call the `listTechniciansRef()` function to get a reference to the query.
const ref = listTechniciansRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listTechniciansRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.technicians);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.technicians);
});
```

## GetAssignment
You can execute the `GetAssignment` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getAssignment(vars: GetAssignmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetAssignmentData, GetAssignmentVariables>;

interface GetAssignmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetAssignmentVariables): QueryRef<GetAssignmentData, GetAssignmentVariables>;
}
export const getAssignmentRef: GetAssignmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getAssignment(dc: DataConnect, vars: GetAssignmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetAssignmentData, GetAssignmentVariables>;

interface GetAssignmentRef {
  ...
  (dc: DataConnect, vars: GetAssignmentVariables): QueryRef<GetAssignmentData, GetAssignmentVariables>;
}
export const getAssignmentRef: GetAssignmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getAssignmentRef:
```typescript
const name = getAssignmentRef.operationName;
console.log(name);
```

### Variables
The `GetAssignment` query requires an argument of type `GetAssignmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetAssignmentVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetAssignment` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetAssignmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetAssignmentData {
  assignment?: {
    assignedDate: TimestampString;
    repairTask: {
      status: string;
    };
  };
}
```
### Using `GetAssignment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getAssignment, GetAssignmentVariables } from '@dataconnect/generated';

// The `GetAssignment` query requires an argument of type `GetAssignmentVariables`:
const getAssignmentVars: GetAssignmentVariables = {
  id: ..., 
};

// Call the `getAssignment()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getAssignment(getAssignmentVars);
// Variables can be defined inline as well.
const { data } = await getAssignment({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getAssignment(dataConnect, getAssignmentVars);

console.log(data.assignment);

// Or, you can use the `Promise` API.
getAssignment(getAssignmentVars).then((response) => {
  const data = response.data;
  console.log(data.assignment);
});
```

### Using `GetAssignment`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getAssignmentRef, GetAssignmentVariables } from '@dataconnect/generated';

// The `GetAssignment` query requires an argument of type `GetAssignmentVariables`:
const getAssignmentVars: GetAssignmentVariables = {
  id: ..., 
};

// Call the `getAssignmentRef()` function to get a reference to the query.
const ref = getAssignmentRef(getAssignmentVars);
// Variables can be defined inline as well.
const ref = getAssignmentRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getAssignmentRef(dataConnect, getAssignmentVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.assignment);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.assignment);
});
```

## ListAssignments
You can execute the `ListAssignments` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listAssignments(options?: ExecuteQueryOptions): QueryPromise<ListAssignmentsData, undefined>;

interface ListAssignmentsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListAssignmentsData, undefined>;
}
export const listAssignmentsRef: ListAssignmentsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listAssignments(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListAssignmentsData, undefined>;

interface ListAssignmentsRef {
  ...
  (dc: DataConnect): QueryRef<ListAssignmentsData, undefined>;
}
export const listAssignmentsRef: ListAssignmentsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listAssignmentsRef:
```typescript
const name = listAssignmentsRef.operationName;
console.log(name);
```

### Variables
The `ListAssignments` query has no variables.
### Return Type
Recall that executing the `ListAssignments` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListAssignmentsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListAssignmentsData {
  assignments: ({
    id: UUIDString;
    assignedDate: TimestampString;
  } & Assignment_Key)[];
}
```
### Using `ListAssignments`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listAssignments } from '@dataconnect/generated';


// Call the `listAssignments()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listAssignments();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listAssignments(dataConnect);

console.log(data.assignments);

// Or, you can use the `Promise` API.
listAssignments().then((response) => {
  const data = response.data;
  console.log(data.assignments);
});
```

### Using `ListAssignments`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listAssignmentsRef } from '@dataconnect/generated';


// Call the `listAssignmentsRef()` function to get a reference to the query.
const ref = listAssignmentsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listAssignmentsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.assignments);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.assignments);
});
```

## GetShipment
You can execute the `GetShipment` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getShipment(vars: GetShipmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetShipmentData, GetShipmentVariables>;

interface GetShipmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetShipmentVariables): QueryRef<GetShipmentData, GetShipmentVariables>;
}
export const getShipmentRef: GetShipmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getShipment(dc: DataConnect, vars: GetShipmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetShipmentData, GetShipmentVariables>;

interface GetShipmentRef {
  ...
  (dc: DataConnect, vars: GetShipmentVariables): QueryRef<GetShipmentData, GetShipmentVariables>;
}
export const getShipmentRef: GetShipmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getShipmentRef:
```typescript
const name = getShipmentRef.operationName;
console.log(name);
```

### Variables
The `GetShipment` query requires an argument of type `GetShipmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetShipmentVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetShipment` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetShipmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetShipmentData {
  shipment?: {
    trackingNumber: string;
    destinationAddress: string;
  };
}
```
### Using `GetShipment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getShipment, GetShipmentVariables } from '@dataconnect/generated';

// The `GetShipment` query requires an argument of type `GetShipmentVariables`:
const getShipmentVars: GetShipmentVariables = {
  id: ..., 
};

// Call the `getShipment()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getShipment(getShipmentVars);
// Variables can be defined inline as well.
const { data } = await getShipment({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getShipment(dataConnect, getShipmentVars);

console.log(data.shipment);

// Or, you can use the `Promise` API.
getShipment(getShipmentVars).then((response) => {
  const data = response.data;
  console.log(data.shipment);
});
```

### Using `GetShipment`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getShipmentRef, GetShipmentVariables } from '@dataconnect/generated';

// The `GetShipment` query requires an argument of type `GetShipmentVariables`:
const getShipmentVars: GetShipmentVariables = {
  id: ..., 
};

// Call the `getShipmentRef()` function to get a reference to the query.
const ref = getShipmentRef(getShipmentVars);
// Variables can be defined inline as well.
const ref = getShipmentRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getShipmentRef(dataConnect, getShipmentVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.shipment);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.shipment);
});
```

## ListShipments
You can execute the `ListShipments` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listShipments(options?: ExecuteQueryOptions): QueryPromise<ListShipmentsData, undefined>;

interface ListShipmentsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListShipmentsData, undefined>;
}
export const listShipmentsRef: ListShipmentsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listShipments(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListShipmentsData, undefined>;

interface ListShipmentsRef {
  ...
  (dc: DataConnect): QueryRef<ListShipmentsData, undefined>;
}
export const listShipmentsRef: ListShipmentsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listShipmentsRef:
```typescript
const name = listShipmentsRef.operationName;
console.log(name);
```

### Variables
The `ListShipments` query has no variables.
### Return Type
Recall that executing the `ListShipments` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListShipmentsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListShipmentsData {
  shipments: ({
    id: UUIDString;
    trackingNumber: string;
  } & Shipment_Key)[];
}
```
### Using `ListShipments`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listShipments } from '@dataconnect/generated';


// Call the `listShipments()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listShipments();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listShipments(dataConnect);

console.log(data.shipments);

// Or, you can use the `Promise` API.
listShipments().then((response) => {
  const data = response.data;
  console.log(data.shipments);
});
```

### Using `ListShipments`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listShipmentsRef } from '@dataconnect/generated';


// Call the `listShipmentsRef()` function to get a reference to the query.
const ref = listShipmentsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listShipmentsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.shipments);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.shipments);
});
```

# Mutations

There are two ways to execute a Data Connect Mutation using the generated Web SDK:
- Using a Mutation Reference function, which returns a `MutationRef`
  - The `MutationRef` can be used as an argument to `executeMutation()`, which will execute the Mutation and return a `MutationPromise`
- Using an action shortcut function, which returns a `MutationPromise`
  - Calling the action shortcut function will execute the Mutation and return a `MutationPromise`

The following is true for both the action shortcut function and the `MutationRef` function:
- The `MutationPromise` returned will resolve to the result of the Mutation once it has finished executing
- If the Mutation accepts arguments, both the action shortcut function and the `MutationRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Mutation
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each mutation. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-mutations).

## CreateItem
You can execute the `CreateItem` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createItem(vars: CreateItemVariables): MutationPromise<CreateItemData, CreateItemVariables>;

interface CreateItemRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateItemVariables): MutationRef<CreateItemData, CreateItemVariables>;
}
export const createItemRef: CreateItemRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createItem(dc: DataConnect, vars: CreateItemVariables): MutationPromise<CreateItemData, CreateItemVariables>;

interface CreateItemRef {
  ...
  (dc: DataConnect, vars: CreateItemVariables): MutationRef<CreateItemData, CreateItemVariables>;
}
export const createItemRef: CreateItemRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createItemRef:
```typescript
const name = createItemRef.operationName;
console.log(name);
```

### Variables
The `CreateItem` mutation requires an argument of type `CreateItemVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateItemVariables {
  name: string;
  initialCondition: string;
  status: string;
}
```
### Return Type
Recall that executing the `CreateItem` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateItemData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateItemData {
  item_insert: Item_Key;
}
```
### Using `CreateItem`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createItem, CreateItemVariables } from '@dataconnect/generated';

// The `CreateItem` mutation requires an argument of type `CreateItemVariables`:
const createItemVars: CreateItemVariables = {
  name: ..., 
  initialCondition: ..., 
  status: ..., 
};

// Call the `createItem()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createItem(createItemVars);
// Variables can be defined inline as well.
const { data } = await createItem({ name: ..., initialCondition: ..., status: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createItem(dataConnect, createItemVars);

console.log(data.item_insert);

// Or, you can use the `Promise` API.
createItem(createItemVars).then((response) => {
  const data = response.data;
  console.log(data.item_insert);
});
```

### Using `CreateItem`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createItemRef, CreateItemVariables } from '@dataconnect/generated';

// The `CreateItem` mutation requires an argument of type `CreateItemVariables`:
const createItemVars: CreateItemVariables = {
  name: ..., 
  initialCondition: ..., 
  status: ..., 
};

// Call the `createItemRef()` function to get a reference to the mutation.
const ref = createItemRef(createItemVars);
// Variables can be defined inline as well.
const ref = createItemRef({ name: ..., initialCondition: ..., status: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createItemRef(dataConnect, createItemVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.item_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.item_insert);
});
```

## UpdateItem
You can execute the `UpdateItem` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateItem(vars: UpdateItemVariables): MutationPromise<UpdateItemData, UpdateItemVariables>;

interface UpdateItemRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateItemVariables): MutationRef<UpdateItemData, UpdateItemVariables>;
}
export const updateItemRef: UpdateItemRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateItem(dc: DataConnect, vars: UpdateItemVariables): MutationPromise<UpdateItemData, UpdateItemVariables>;

interface UpdateItemRef {
  ...
  (dc: DataConnect, vars: UpdateItemVariables): MutationRef<UpdateItemData, UpdateItemVariables>;
}
export const updateItemRef: UpdateItemRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateItemRef:
```typescript
const name = updateItemRef.operationName;
console.log(name);
```

### Variables
The `UpdateItem` mutation requires an argument of type `UpdateItemVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateItemVariables {
  id: UUIDString;
  status: string;
}
```
### Return Type
Recall that executing the `UpdateItem` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateItemData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateItemData {
  item_update?: Item_Key | null;
}
```
### Using `UpdateItem`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateItem, UpdateItemVariables } from '@dataconnect/generated';

// The `UpdateItem` mutation requires an argument of type `UpdateItemVariables`:
const updateItemVars: UpdateItemVariables = {
  id: ..., 
  status: ..., 
};

// Call the `updateItem()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateItem(updateItemVars);
// Variables can be defined inline as well.
const { data } = await updateItem({ id: ..., status: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateItem(dataConnect, updateItemVars);

console.log(data.item_update);

// Or, you can use the `Promise` API.
updateItem(updateItemVars).then((response) => {
  const data = response.data;
  console.log(data.item_update);
});
```

### Using `UpdateItem`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateItemRef, UpdateItemVariables } from '@dataconnect/generated';

// The `UpdateItem` mutation requires an argument of type `UpdateItemVariables`:
const updateItemVars: UpdateItemVariables = {
  id: ..., 
  status: ..., 
};

// Call the `updateItemRef()` function to get a reference to the mutation.
const ref = updateItemRef(updateItemVars);
// Variables can be defined inline as well.
const ref = updateItemRef({ id: ..., status: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateItemRef(dataConnect, updateItemVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.item_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.item_update);
});
```

## DeleteItem
You can execute the `DeleteItem` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteItem(vars: DeleteItemVariables): MutationPromise<DeleteItemData, DeleteItemVariables>;

interface DeleteItemRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteItemVariables): MutationRef<DeleteItemData, DeleteItemVariables>;
}
export const deleteItemRef: DeleteItemRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteItem(dc: DataConnect, vars: DeleteItemVariables): MutationPromise<DeleteItemData, DeleteItemVariables>;

interface DeleteItemRef {
  ...
  (dc: DataConnect, vars: DeleteItemVariables): MutationRef<DeleteItemData, DeleteItemVariables>;
}
export const deleteItemRef: DeleteItemRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteItemRef:
```typescript
const name = deleteItemRef.operationName;
console.log(name);
```

### Variables
The `DeleteItem` mutation requires an argument of type `DeleteItemVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteItemVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteItem` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteItemData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteItemData {
  item_delete?: Item_Key | null;
}
```
### Using `DeleteItem`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteItem, DeleteItemVariables } from '@dataconnect/generated';

// The `DeleteItem` mutation requires an argument of type `DeleteItemVariables`:
const deleteItemVars: DeleteItemVariables = {
  id: ..., 
};

// Call the `deleteItem()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteItem(deleteItemVars);
// Variables can be defined inline as well.
const { data } = await deleteItem({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteItem(dataConnect, deleteItemVars);

console.log(data.item_delete);

// Or, you can use the `Promise` API.
deleteItem(deleteItemVars).then((response) => {
  const data = response.data;
  console.log(data.item_delete);
});
```

### Using `DeleteItem`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteItemRef, DeleteItemVariables } from '@dataconnect/generated';

// The `DeleteItem` mutation requires an argument of type `DeleteItemVariables`:
const deleteItemVars: DeleteItemVariables = {
  id: ..., 
};

// Call the `deleteItemRef()` function to get a reference to the mutation.
const ref = deleteItemRef(deleteItemVars);
// Variables can be defined inline as well.
const ref = deleteItemRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteItemRef(dataConnect, deleteItemVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.item_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.item_delete);
});
```

## CreateRepairTask
You can execute the `CreateRepairTask` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createRepairTask(vars: CreateRepairTaskVariables): MutationPromise<CreateRepairTaskData, CreateRepairTaskVariables>;

interface CreateRepairTaskRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateRepairTaskVariables): MutationRef<CreateRepairTaskData, CreateRepairTaskVariables>;
}
export const createRepairTaskRef: CreateRepairTaskRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createRepairTask(dc: DataConnect, vars: CreateRepairTaskVariables): MutationPromise<CreateRepairTaskData, CreateRepairTaskVariables>;

interface CreateRepairTaskRef {
  ...
  (dc: DataConnect, vars: CreateRepairTaskVariables): MutationRef<CreateRepairTaskData, CreateRepairTaskVariables>;
}
export const createRepairTaskRef: CreateRepairTaskRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createRepairTaskRef:
```typescript
const name = createRepairTaskRef.operationName;
console.log(name);
```

### Variables
The `CreateRepairTask` mutation requires an argument of type `CreateRepairTaskVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateRepairTaskVariables {
  startDate: TimestampString;
  status: string;
  itemId: UUIDString;
}
```
### Return Type
Recall that executing the `CreateRepairTask` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateRepairTaskData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateRepairTaskData {
  repairTask_insert: RepairTask_Key;
}
```
### Using `CreateRepairTask`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createRepairTask, CreateRepairTaskVariables } from '@dataconnect/generated';

// The `CreateRepairTask` mutation requires an argument of type `CreateRepairTaskVariables`:
const createRepairTaskVars: CreateRepairTaskVariables = {
  startDate: ..., 
  status: ..., 
  itemId: ..., 
};

// Call the `createRepairTask()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createRepairTask(createRepairTaskVars);
// Variables can be defined inline as well.
const { data } = await createRepairTask({ startDate: ..., status: ..., itemId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createRepairTask(dataConnect, createRepairTaskVars);

console.log(data.repairTask_insert);

// Or, you can use the `Promise` API.
createRepairTask(createRepairTaskVars).then((response) => {
  const data = response.data;
  console.log(data.repairTask_insert);
});
```

### Using `CreateRepairTask`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createRepairTaskRef, CreateRepairTaskVariables } from '@dataconnect/generated';

// The `CreateRepairTask` mutation requires an argument of type `CreateRepairTaskVariables`:
const createRepairTaskVars: CreateRepairTaskVariables = {
  startDate: ..., 
  status: ..., 
  itemId: ..., 
};

// Call the `createRepairTaskRef()` function to get a reference to the mutation.
const ref = createRepairTaskRef(createRepairTaskVars);
// Variables can be defined inline as well.
const ref = createRepairTaskRef({ startDate: ..., status: ..., itemId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createRepairTaskRef(dataConnect, createRepairTaskVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.repairTask_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.repairTask_insert);
});
```

## UpdateRepairTask
You can execute the `UpdateRepairTask` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateRepairTask(vars: UpdateRepairTaskVariables): MutationPromise<UpdateRepairTaskData, UpdateRepairTaskVariables>;

interface UpdateRepairTaskRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateRepairTaskVariables): MutationRef<UpdateRepairTaskData, UpdateRepairTaskVariables>;
}
export const updateRepairTaskRef: UpdateRepairTaskRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateRepairTask(dc: DataConnect, vars: UpdateRepairTaskVariables): MutationPromise<UpdateRepairTaskData, UpdateRepairTaskVariables>;

interface UpdateRepairTaskRef {
  ...
  (dc: DataConnect, vars: UpdateRepairTaskVariables): MutationRef<UpdateRepairTaskData, UpdateRepairTaskVariables>;
}
export const updateRepairTaskRef: UpdateRepairTaskRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateRepairTaskRef:
```typescript
const name = updateRepairTaskRef.operationName;
console.log(name);
```

### Variables
The `UpdateRepairTask` mutation requires an argument of type `UpdateRepairTaskVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateRepairTaskVariables {
  id: UUIDString;
  notes?: string | null;
}
```
### Return Type
Recall that executing the `UpdateRepairTask` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateRepairTaskData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateRepairTaskData {
  repairTask_update?: RepairTask_Key | null;
}
```
### Using `UpdateRepairTask`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateRepairTask, UpdateRepairTaskVariables } from '@dataconnect/generated';

// The `UpdateRepairTask` mutation requires an argument of type `UpdateRepairTaskVariables`:
const updateRepairTaskVars: UpdateRepairTaskVariables = {
  id: ..., 
  notes: ..., // optional
};

// Call the `updateRepairTask()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateRepairTask(updateRepairTaskVars);
// Variables can be defined inline as well.
const { data } = await updateRepairTask({ id: ..., notes: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateRepairTask(dataConnect, updateRepairTaskVars);

console.log(data.repairTask_update);

// Or, you can use the `Promise` API.
updateRepairTask(updateRepairTaskVars).then((response) => {
  const data = response.data;
  console.log(data.repairTask_update);
});
```

### Using `UpdateRepairTask`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateRepairTaskRef, UpdateRepairTaskVariables } from '@dataconnect/generated';

// The `UpdateRepairTask` mutation requires an argument of type `UpdateRepairTaskVariables`:
const updateRepairTaskVars: UpdateRepairTaskVariables = {
  id: ..., 
  notes: ..., // optional
};

// Call the `updateRepairTaskRef()` function to get a reference to the mutation.
const ref = updateRepairTaskRef(updateRepairTaskVars);
// Variables can be defined inline as well.
const ref = updateRepairTaskRef({ id: ..., notes: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateRepairTaskRef(dataConnect, updateRepairTaskVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.repairTask_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.repairTask_update);
});
```

## DeleteRepairTask
You can execute the `DeleteRepairTask` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteRepairTask(vars: DeleteRepairTaskVariables): MutationPromise<DeleteRepairTaskData, DeleteRepairTaskVariables>;

interface DeleteRepairTaskRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteRepairTaskVariables): MutationRef<DeleteRepairTaskData, DeleteRepairTaskVariables>;
}
export const deleteRepairTaskRef: DeleteRepairTaskRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteRepairTask(dc: DataConnect, vars: DeleteRepairTaskVariables): MutationPromise<DeleteRepairTaskData, DeleteRepairTaskVariables>;

interface DeleteRepairTaskRef {
  ...
  (dc: DataConnect, vars: DeleteRepairTaskVariables): MutationRef<DeleteRepairTaskData, DeleteRepairTaskVariables>;
}
export const deleteRepairTaskRef: DeleteRepairTaskRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteRepairTaskRef:
```typescript
const name = deleteRepairTaskRef.operationName;
console.log(name);
```

### Variables
The `DeleteRepairTask` mutation requires an argument of type `DeleteRepairTaskVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteRepairTaskVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteRepairTask` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteRepairTaskData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteRepairTaskData {
  repairTask_delete?: RepairTask_Key | null;
}
```
### Using `DeleteRepairTask`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteRepairTask, DeleteRepairTaskVariables } from '@dataconnect/generated';

// The `DeleteRepairTask` mutation requires an argument of type `DeleteRepairTaskVariables`:
const deleteRepairTaskVars: DeleteRepairTaskVariables = {
  id: ..., 
};

// Call the `deleteRepairTask()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteRepairTask(deleteRepairTaskVars);
// Variables can be defined inline as well.
const { data } = await deleteRepairTask({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteRepairTask(dataConnect, deleteRepairTaskVars);

console.log(data.repairTask_delete);

// Or, you can use the `Promise` API.
deleteRepairTask(deleteRepairTaskVars).then((response) => {
  const data = response.data;
  console.log(data.repairTask_delete);
});
```

### Using `DeleteRepairTask`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteRepairTaskRef, DeleteRepairTaskVariables } from '@dataconnect/generated';

// The `DeleteRepairTask` mutation requires an argument of type `DeleteRepairTaskVariables`:
const deleteRepairTaskVars: DeleteRepairTaskVariables = {
  id: ..., 
};

// Call the `deleteRepairTaskRef()` function to get a reference to the mutation.
const ref = deleteRepairTaskRef(deleteRepairTaskVars);
// Variables can be defined inline as well.
const ref = deleteRepairTaskRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteRepairTaskRef(dataConnect, deleteRepairTaskVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.repairTask_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.repairTask_delete);
});
```

## CreateTechnician
You can execute the `CreateTechnician` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createTechnician(vars: CreateTechnicianVariables): MutationPromise<CreateTechnicianData, CreateTechnicianVariables>;

interface CreateTechnicianRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateTechnicianVariables): MutationRef<CreateTechnicianData, CreateTechnicianVariables>;
}
export const createTechnicianRef: CreateTechnicianRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createTechnician(dc: DataConnect, vars: CreateTechnicianVariables): MutationPromise<CreateTechnicianData, CreateTechnicianVariables>;

interface CreateTechnicianRef {
  ...
  (dc: DataConnect, vars: CreateTechnicianVariables): MutationRef<CreateTechnicianData, CreateTechnicianVariables>;
}
export const createTechnicianRef: CreateTechnicianRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createTechnicianRef:
```typescript
const name = createTechnicianRef.operationName;
console.log(name);
```

### Variables
The `CreateTechnician` mutation requires an argument of type `CreateTechnicianVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateTechnicianVariables {
  name: string;
  email: string;
}
```
### Return Type
Recall that executing the `CreateTechnician` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateTechnicianData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateTechnicianData {
  technician_insert: Technician_Key;
}
```
### Using `CreateTechnician`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createTechnician, CreateTechnicianVariables } from '@dataconnect/generated';

// The `CreateTechnician` mutation requires an argument of type `CreateTechnicianVariables`:
const createTechnicianVars: CreateTechnicianVariables = {
  name: ..., 
  email: ..., 
};

// Call the `createTechnician()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createTechnician(createTechnicianVars);
// Variables can be defined inline as well.
const { data } = await createTechnician({ name: ..., email: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createTechnician(dataConnect, createTechnicianVars);

console.log(data.technician_insert);

// Or, you can use the `Promise` API.
createTechnician(createTechnicianVars).then((response) => {
  const data = response.data;
  console.log(data.technician_insert);
});
```

### Using `CreateTechnician`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createTechnicianRef, CreateTechnicianVariables } from '@dataconnect/generated';

// The `CreateTechnician` mutation requires an argument of type `CreateTechnicianVariables`:
const createTechnicianVars: CreateTechnicianVariables = {
  name: ..., 
  email: ..., 
};

// Call the `createTechnicianRef()` function to get a reference to the mutation.
const ref = createTechnicianRef(createTechnicianVars);
// Variables can be defined inline as well.
const ref = createTechnicianRef({ name: ..., email: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createTechnicianRef(dataConnect, createTechnicianVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.technician_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.technician_insert);
});
```

## UpdateTechnician
You can execute the `UpdateTechnician` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateTechnician(vars: UpdateTechnicianVariables): MutationPromise<UpdateTechnicianData, UpdateTechnicianVariables>;

interface UpdateTechnicianRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateTechnicianVariables): MutationRef<UpdateTechnicianData, UpdateTechnicianVariables>;
}
export const updateTechnicianRef: UpdateTechnicianRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateTechnician(dc: DataConnect, vars: UpdateTechnicianVariables): MutationPromise<UpdateTechnicianData, UpdateTechnicianVariables>;

interface UpdateTechnicianRef {
  ...
  (dc: DataConnect, vars: UpdateTechnicianVariables): MutationRef<UpdateTechnicianData, UpdateTechnicianVariables>;
}
export const updateTechnicianRef: UpdateTechnicianRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateTechnicianRef:
```typescript
const name = updateTechnicianRef.operationName;
console.log(name);
```

### Variables
The `UpdateTechnician` mutation requires an argument of type `UpdateTechnicianVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateTechnicianVariables {
  id: UUIDString;
  specialty?: string | null;
}
```
### Return Type
Recall that executing the `UpdateTechnician` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateTechnicianData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateTechnicianData {
  technician_update?: Technician_Key | null;
}
```
### Using `UpdateTechnician`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateTechnician, UpdateTechnicianVariables } from '@dataconnect/generated';

// The `UpdateTechnician` mutation requires an argument of type `UpdateTechnicianVariables`:
const updateTechnicianVars: UpdateTechnicianVariables = {
  id: ..., 
  specialty: ..., // optional
};

// Call the `updateTechnician()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateTechnician(updateTechnicianVars);
// Variables can be defined inline as well.
const { data } = await updateTechnician({ id: ..., specialty: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateTechnician(dataConnect, updateTechnicianVars);

console.log(data.technician_update);

// Or, you can use the `Promise` API.
updateTechnician(updateTechnicianVars).then((response) => {
  const data = response.data;
  console.log(data.technician_update);
});
```

### Using `UpdateTechnician`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateTechnicianRef, UpdateTechnicianVariables } from '@dataconnect/generated';

// The `UpdateTechnician` mutation requires an argument of type `UpdateTechnicianVariables`:
const updateTechnicianVars: UpdateTechnicianVariables = {
  id: ..., 
  specialty: ..., // optional
};

// Call the `updateTechnicianRef()` function to get a reference to the mutation.
const ref = updateTechnicianRef(updateTechnicianVars);
// Variables can be defined inline as well.
const ref = updateTechnicianRef({ id: ..., specialty: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateTechnicianRef(dataConnect, updateTechnicianVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.technician_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.technician_update);
});
```

## DeleteTechnician
You can execute the `DeleteTechnician` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteTechnician(vars: DeleteTechnicianVariables): MutationPromise<DeleteTechnicianData, DeleteTechnicianVariables>;

interface DeleteTechnicianRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteTechnicianVariables): MutationRef<DeleteTechnicianData, DeleteTechnicianVariables>;
}
export const deleteTechnicianRef: DeleteTechnicianRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteTechnician(dc: DataConnect, vars: DeleteTechnicianVariables): MutationPromise<DeleteTechnicianData, DeleteTechnicianVariables>;

interface DeleteTechnicianRef {
  ...
  (dc: DataConnect, vars: DeleteTechnicianVariables): MutationRef<DeleteTechnicianData, DeleteTechnicianVariables>;
}
export const deleteTechnicianRef: DeleteTechnicianRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteTechnicianRef:
```typescript
const name = deleteTechnicianRef.operationName;
console.log(name);
```

### Variables
The `DeleteTechnician` mutation requires an argument of type `DeleteTechnicianVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteTechnicianVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteTechnician` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteTechnicianData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteTechnicianData {
  technician_delete?: Technician_Key | null;
}
```
### Using `DeleteTechnician`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteTechnician, DeleteTechnicianVariables } from '@dataconnect/generated';

// The `DeleteTechnician` mutation requires an argument of type `DeleteTechnicianVariables`:
const deleteTechnicianVars: DeleteTechnicianVariables = {
  id: ..., 
};

// Call the `deleteTechnician()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteTechnician(deleteTechnicianVars);
// Variables can be defined inline as well.
const { data } = await deleteTechnician({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteTechnician(dataConnect, deleteTechnicianVars);

console.log(data.technician_delete);

// Or, you can use the `Promise` API.
deleteTechnician(deleteTechnicianVars).then((response) => {
  const data = response.data;
  console.log(data.technician_delete);
});
```

### Using `DeleteTechnician`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteTechnicianRef, DeleteTechnicianVariables } from '@dataconnect/generated';

// The `DeleteTechnician` mutation requires an argument of type `DeleteTechnicianVariables`:
const deleteTechnicianVars: DeleteTechnicianVariables = {
  id: ..., 
};

// Call the `deleteTechnicianRef()` function to get a reference to the mutation.
const ref = deleteTechnicianRef(deleteTechnicianVars);
// Variables can be defined inline as well.
const ref = deleteTechnicianRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteTechnicianRef(dataConnect, deleteTechnicianVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.technician_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.technician_delete);
});
```

## CreateAssignment
You can execute the `CreateAssignment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createAssignment(vars: CreateAssignmentVariables): MutationPromise<CreateAssignmentData, CreateAssignmentVariables>;

interface CreateAssignmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateAssignmentVariables): MutationRef<CreateAssignmentData, CreateAssignmentVariables>;
}
export const createAssignmentRef: CreateAssignmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createAssignment(dc: DataConnect, vars: CreateAssignmentVariables): MutationPromise<CreateAssignmentData, CreateAssignmentVariables>;

interface CreateAssignmentRef {
  ...
  (dc: DataConnect, vars: CreateAssignmentVariables): MutationRef<CreateAssignmentData, CreateAssignmentVariables>;
}
export const createAssignmentRef: CreateAssignmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createAssignmentRef:
```typescript
const name = createAssignmentRef.operationName;
console.log(name);
```

### Variables
The `CreateAssignment` mutation requires an argument of type `CreateAssignmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateAssignmentVariables {
  assignedDate: TimestampString;
  repairTaskId: UUIDString;
  technicianId: UUIDString;
}
```
### Return Type
Recall that executing the `CreateAssignment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateAssignmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateAssignmentData {
  assignment_insert: Assignment_Key;
}
```
### Using `CreateAssignment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createAssignment, CreateAssignmentVariables } from '@dataconnect/generated';

// The `CreateAssignment` mutation requires an argument of type `CreateAssignmentVariables`:
const createAssignmentVars: CreateAssignmentVariables = {
  assignedDate: ..., 
  repairTaskId: ..., 
  technicianId: ..., 
};

// Call the `createAssignment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createAssignment(createAssignmentVars);
// Variables can be defined inline as well.
const { data } = await createAssignment({ assignedDate: ..., repairTaskId: ..., technicianId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createAssignment(dataConnect, createAssignmentVars);

console.log(data.assignment_insert);

// Or, you can use the `Promise` API.
createAssignment(createAssignmentVars).then((response) => {
  const data = response.data;
  console.log(data.assignment_insert);
});
```

### Using `CreateAssignment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createAssignmentRef, CreateAssignmentVariables } from '@dataconnect/generated';

// The `CreateAssignment` mutation requires an argument of type `CreateAssignmentVariables`:
const createAssignmentVars: CreateAssignmentVariables = {
  assignedDate: ..., 
  repairTaskId: ..., 
  technicianId: ..., 
};

// Call the `createAssignmentRef()` function to get a reference to the mutation.
const ref = createAssignmentRef(createAssignmentVars);
// Variables can be defined inline as well.
const ref = createAssignmentRef({ assignedDate: ..., repairTaskId: ..., technicianId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createAssignmentRef(dataConnect, createAssignmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.assignment_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.assignment_insert);
});
```

## UpdateAssignment
You can execute the `UpdateAssignment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateAssignment(vars: UpdateAssignmentVariables): MutationPromise<UpdateAssignmentData, UpdateAssignmentVariables>;

interface UpdateAssignmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateAssignmentVariables): MutationRef<UpdateAssignmentData, UpdateAssignmentVariables>;
}
export const updateAssignmentRef: UpdateAssignmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateAssignment(dc: DataConnect, vars: UpdateAssignmentVariables): MutationPromise<UpdateAssignmentData, UpdateAssignmentVariables>;

interface UpdateAssignmentRef {
  ...
  (dc: DataConnect, vars: UpdateAssignmentVariables): MutationRef<UpdateAssignmentData, UpdateAssignmentVariables>;
}
export const updateAssignmentRef: UpdateAssignmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateAssignmentRef:
```typescript
const name = updateAssignmentRef.operationName;
console.log(name);
```

### Variables
The `UpdateAssignment` mutation requires an argument of type `UpdateAssignmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateAssignmentVariables {
  id: UUIDString;
  priorityLevel?: number | null;
}
```
### Return Type
Recall that executing the `UpdateAssignment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateAssignmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateAssignmentData {
  assignment_update?: Assignment_Key | null;
}
```
### Using `UpdateAssignment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateAssignment, UpdateAssignmentVariables } from '@dataconnect/generated';

// The `UpdateAssignment` mutation requires an argument of type `UpdateAssignmentVariables`:
const updateAssignmentVars: UpdateAssignmentVariables = {
  id: ..., 
  priorityLevel: ..., // optional
};

// Call the `updateAssignment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateAssignment(updateAssignmentVars);
// Variables can be defined inline as well.
const { data } = await updateAssignment({ id: ..., priorityLevel: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateAssignment(dataConnect, updateAssignmentVars);

console.log(data.assignment_update);

// Or, you can use the `Promise` API.
updateAssignment(updateAssignmentVars).then((response) => {
  const data = response.data;
  console.log(data.assignment_update);
});
```

### Using `UpdateAssignment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateAssignmentRef, UpdateAssignmentVariables } from '@dataconnect/generated';

// The `UpdateAssignment` mutation requires an argument of type `UpdateAssignmentVariables`:
const updateAssignmentVars: UpdateAssignmentVariables = {
  id: ..., 
  priorityLevel: ..., // optional
};

// Call the `updateAssignmentRef()` function to get a reference to the mutation.
const ref = updateAssignmentRef(updateAssignmentVars);
// Variables can be defined inline as well.
const ref = updateAssignmentRef({ id: ..., priorityLevel: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateAssignmentRef(dataConnect, updateAssignmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.assignment_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.assignment_update);
});
```

## DeleteAssignment
You can execute the `DeleteAssignment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteAssignment(vars: DeleteAssignmentVariables): MutationPromise<DeleteAssignmentData, DeleteAssignmentVariables>;

interface DeleteAssignmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteAssignmentVariables): MutationRef<DeleteAssignmentData, DeleteAssignmentVariables>;
}
export const deleteAssignmentRef: DeleteAssignmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteAssignment(dc: DataConnect, vars: DeleteAssignmentVariables): MutationPromise<DeleteAssignmentData, DeleteAssignmentVariables>;

interface DeleteAssignmentRef {
  ...
  (dc: DataConnect, vars: DeleteAssignmentVariables): MutationRef<DeleteAssignmentData, DeleteAssignmentVariables>;
}
export const deleteAssignmentRef: DeleteAssignmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteAssignmentRef:
```typescript
const name = deleteAssignmentRef.operationName;
console.log(name);
```

### Variables
The `DeleteAssignment` mutation requires an argument of type `DeleteAssignmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteAssignmentVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteAssignment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteAssignmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteAssignmentData {
  assignment_delete?: Assignment_Key | null;
}
```
### Using `DeleteAssignment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteAssignment, DeleteAssignmentVariables } from '@dataconnect/generated';

// The `DeleteAssignment` mutation requires an argument of type `DeleteAssignmentVariables`:
const deleteAssignmentVars: DeleteAssignmentVariables = {
  id: ..., 
};

// Call the `deleteAssignment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteAssignment(deleteAssignmentVars);
// Variables can be defined inline as well.
const { data } = await deleteAssignment({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteAssignment(dataConnect, deleteAssignmentVars);

console.log(data.assignment_delete);

// Or, you can use the `Promise` API.
deleteAssignment(deleteAssignmentVars).then((response) => {
  const data = response.data;
  console.log(data.assignment_delete);
});
```

### Using `DeleteAssignment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteAssignmentRef, DeleteAssignmentVariables } from '@dataconnect/generated';

// The `DeleteAssignment` mutation requires an argument of type `DeleteAssignmentVariables`:
const deleteAssignmentVars: DeleteAssignmentVariables = {
  id: ..., 
};

// Call the `deleteAssignmentRef()` function to get a reference to the mutation.
const ref = deleteAssignmentRef(deleteAssignmentVars);
// Variables can be defined inline as well.
const ref = deleteAssignmentRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteAssignmentRef(dataConnect, deleteAssignmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.assignment_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.assignment_delete);
});
```

## CreateShipment
You can execute the `CreateShipment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createShipment(vars: CreateShipmentVariables): MutationPromise<CreateShipmentData, CreateShipmentVariables>;

interface CreateShipmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateShipmentVariables): MutationRef<CreateShipmentData, CreateShipmentVariables>;
}
export const createShipmentRef: CreateShipmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createShipment(dc: DataConnect, vars: CreateShipmentVariables): MutationPromise<CreateShipmentData, CreateShipmentVariables>;

interface CreateShipmentRef {
  ...
  (dc: DataConnect, vars: CreateShipmentVariables): MutationRef<CreateShipmentData, CreateShipmentVariables>;
}
export const createShipmentRef: CreateShipmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createShipmentRef:
```typescript
const name = createShipmentRef.operationName;
console.log(name);
```

### Variables
The `CreateShipment` mutation requires an argument of type `CreateShipmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateShipmentVariables {
  trackingNumber: string;
  destinationAddress: string;
  shipDate: DateString;
  itemId: UUIDString;
}
```
### Return Type
Recall that executing the `CreateShipment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateShipmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateShipmentData {
  shipment_insert: Shipment_Key;
}
```
### Using `CreateShipment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createShipment, CreateShipmentVariables } from '@dataconnect/generated';

// The `CreateShipment` mutation requires an argument of type `CreateShipmentVariables`:
const createShipmentVars: CreateShipmentVariables = {
  trackingNumber: ..., 
  destinationAddress: ..., 
  shipDate: ..., 
  itemId: ..., 
};

// Call the `createShipment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createShipment(createShipmentVars);
// Variables can be defined inline as well.
const { data } = await createShipment({ trackingNumber: ..., destinationAddress: ..., shipDate: ..., itemId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createShipment(dataConnect, createShipmentVars);

console.log(data.shipment_insert);

// Or, you can use the `Promise` API.
createShipment(createShipmentVars).then((response) => {
  const data = response.data;
  console.log(data.shipment_insert);
});
```

### Using `CreateShipment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createShipmentRef, CreateShipmentVariables } from '@dataconnect/generated';

// The `CreateShipment` mutation requires an argument of type `CreateShipmentVariables`:
const createShipmentVars: CreateShipmentVariables = {
  trackingNumber: ..., 
  destinationAddress: ..., 
  shipDate: ..., 
  itemId: ..., 
};

// Call the `createShipmentRef()` function to get a reference to the mutation.
const ref = createShipmentRef(createShipmentVars);
// Variables can be defined inline as well.
const ref = createShipmentRef({ trackingNumber: ..., destinationAddress: ..., shipDate: ..., itemId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createShipmentRef(dataConnect, createShipmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.shipment_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.shipment_insert);
});
```

## UpdateShipment
You can execute the `UpdateShipment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateShipment(vars: UpdateShipmentVariables): MutationPromise<UpdateShipmentData, UpdateShipmentVariables>;

interface UpdateShipmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateShipmentVariables): MutationRef<UpdateShipmentData, UpdateShipmentVariables>;
}
export const updateShipmentRef: UpdateShipmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateShipment(dc: DataConnect, vars: UpdateShipmentVariables): MutationPromise<UpdateShipmentData, UpdateShipmentVariables>;

interface UpdateShipmentRef {
  ...
  (dc: DataConnect, vars: UpdateShipmentVariables): MutationRef<UpdateShipmentData, UpdateShipmentVariables>;
}
export const updateShipmentRef: UpdateShipmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateShipmentRef:
```typescript
const name = updateShipmentRef.operationName;
console.log(name);
```

### Variables
The `UpdateShipment` mutation requires an argument of type `UpdateShipmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateShipmentVariables {
  id: UUIDString;
  carrierName?: string | null;
}
```
### Return Type
Recall that executing the `UpdateShipment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateShipmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateShipmentData {
  shipment_update?: Shipment_Key | null;
}
```
### Using `UpdateShipment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateShipment, UpdateShipmentVariables } from '@dataconnect/generated';

// The `UpdateShipment` mutation requires an argument of type `UpdateShipmentVariables`:
const updateShipmentVars: UpdateShipmentVariables = {
  id: ..., 
  carrierName: ..., // optional
};

// Call the `updateShipment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateShipment(updateShipmentVars);
// Variables can be defined inline as well.
const { data } = await updateShipment({ id: ..., carrierName: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateShipment(dataConnect, updateShipmentVars);

console.log(data.shipment_update);

// Or, you can use the `Promise` API.
updateShipment(updateShipmentVars).then((response) => {
  const data = response.data;
  console.log(data.shipment_update);
});
```

### Using `UpdateShipment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateShipmentRef, UpdateShipmentVariables } from '@dataconnect/generated';

// The `UpdateShipment` mutation requires an argument of type `UpdateShipmentVariables`:
const updateShipmentVars: UpdateShipmentVariables = {
  id: ..., 
  carrierName: ..., // optional
};

// Call the `updateShipmentRef()` function to get a reference to the mutation.
const ref = updateShipmentRef(updateShipmentVars);
// Variables can be defined inline as well.
const ref = updateShipmentRef({ id: ..., carrierName: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateShipmentRef(dataConnect, updateShipmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.shipment_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.shipment_update);
});
```

## DeleteShipment
You can execute the `DeleteShipment` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteShipment(vars: DeleteShipmentVariables): MutationPromise<DeleteShipmentData, DeleteShipmentVariables>;

interface DeleteShipmentRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteShipmentVariables): MutationRef<DeleteShipmentData, DeleteShipmentVariables>;
}
export const deleteShipmentRef: DeleteShipmentRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteShipment(dc: DataConnect, vars: DeleteShipmentVariables): MutationPromise<DeleteShipmentData, DeleteShipmentVariables>;

interface DeleteShipmentRef {
  ...
  (dc: DataConnect, vars: DeleteShipmentVariables): MutationRef<DeleteShipmentData, DeleteShipmentVariables>;
}
export const deleteShipmentRef: DeleteShipmentRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteShipmentRef:
```typescript
const name = deleteShipmentRef.operationName;
console.log(name);
```

### Variables
The `DeleteShipment` mutation requires an argument of type `DeleteShipmentVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteShipmentVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteShipment` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteShipmentData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteShipmentData {
  shipment_delete?: Shipment_Key | null;
}
```
### Using `DeleteShipment`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteShipment, DeleteShipmentVariables } from '@dataconnect/generated';

// The `DeleteShipment` mutation requires an argument of type `DeleteShipmentVariables`:
const deleteShipmentVars: DeleteShipmentVariables = {
  id: ..., 
};

// Call the `deleteShipment()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteShipment(deleteShipmentVars);
// Variables can be defined inline as well.
const { data } = await deleteShipment({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteShipment(dataConnect, deleteShipmentVars);

console.log(data.shipment_delete);

// Or, you can use the `Promise` API.
deleteShipment(deleteShipmentVars).then((response) => {
  const data = response.data;
  console.log(data.shipment_delete);
});
```

### Using `DeleteShipment`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteShipmentRef, DeleteShipmentVariables } from '@dataconnect/generated';

// The `DeleteShipment` mutation requires an argument of type `DeleteShipmentVariables`:
const deleteShipmentVars: DeleteShipmentVariables = {
  id: ..., 
};

// Call the `deleteShipmentRef()` function to get a reference to the mutation.
const ref = deleteShipmentRef(deleteShipmentVars);
// Variables can be defined inline as well.
const ref = deleteShipmentRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteShipmentRef(dataConnect, deleteShipmentVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.shipment_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.shipment_delete);
});
```

