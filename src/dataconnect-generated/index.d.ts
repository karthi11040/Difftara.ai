import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, ExecuteQueryOptions, MutationRef, MutationPromise, DataConnectSettings } from 'firebase/data-connect';

export const connectorConfig: ConnectorConfig;
export const dataConnectSettings: DataConnectSettings;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;




export interface Assignment_Key {
  id: UUIDString;
  __typename?: 'Assignment_Key';
}

export interface CreateAssignmentData {
  assignment_insert: Assignment_Key;
}

export interface CreateAssignmentVariables {
  assignedDate: TimestampString;
  repairTaskId: UUIDString;
  technicianId: UUIDString;
}

export interface CreateItemData {
  item_insert: Item_Key;
}

export interface CreateItemVariables {
  name: string;
  initialCondition: string;
  status: string;
}

export interface CreateRepairTaskData {
  repairTask_insert: RepairTask_Key;
}

export interface CreateRepairTaskVariables {
  startDate: TimestampString;
  status: string;
  itemId: UUIDString;
}

export interface CreateShipmentData {
  shipment_insert: Shipment_Key;
}

export interface CreateShipmentVariables {
  trackingNumber: string;
  destinationAddress: string;
  shipDate: DateString;
  itemId: UUIDString;
}

export interface CreateTechnicianData {
  technician_insert: Technician_Key;
}

export interface CreateTechnicianVariables {
  name: string;
  email: string;
}

export interface DeleteAssignmentData {
  assignment_delete?: Assignment_Key | null;
}

export interface DeleteAssignmentVariables {
  id: UUIDString;
}

export interface DeleteItemData {
  item_delete?: Item_Key | null;
}

export interface DeleteItemVariables {
  id: UUIDString;
}

export interface DeleteRepairTaskData {
  repairTask_delete?: RepairTask_Key | null;
}

export interface DeleteRepairTaskVariables {
  id: UUIDString;
}

export interface DeleteShipmentData {
  shipment_delete?: Shipment_Key | null;
}

export interface DeleteShipmentVariables {
  id: UUIDString;
}

export interface DeleteTechnicianData {
  technician_delete?: Technician_Key | null;
}

export interface DeleteTechnicianVariables {
  id: UUIDString;
}

export interface GetAssignmentData {
  assignment?: {
    assignedDate: TimestampString;
    repairTask: {
      status: string;
    };
  };
}

export interface GetAssignmentVariables {
  id: UUIDString;
}

export interface GetItemData {
  item?: {
    name: string;
    status: string;
  };
}

export interface GetItemVariables {
  id: UUIDString;
}

export interface GetRepairTaskData {
  repairTask?: {
    startDate: TimestampString;
    status: string;
    item: {
      name: string;
    };
  };
}

export interface GetRepairTaskVariables {
  id: UUIDString;
}

export interface GetShipmentData {
  shipment?: {
    trackingNumber: string;
    destinationAddress: string;
  };
}

export interface GetShipmentVariables {
  id: UUIDString;
}

export interface GetTechnicianData {
  technician?: {
    name: string;
    email: string;
    specialty?: string | null;
  };
}

export interface GetTechnicianVariables {
  id: UUIDString;
}

export interface Item_Key {
  id: UUIDString;
  __typename?: 'Item_Key';
}

export interface ListAssignmentsData {
  assignments: ({
    id: UUIDString;
    assignedDate: TimestampString;
  } & Assignment_Key)[];
}

export interface ListItemsData {
  items: ({
    id: UUIDString;
    name: string;
    status: string;
  } & Item_Key)[];
}

export interface ListRepairTasksData {
  repairTasks: ({
    id: UUIDString;
    startDate: TimestampString;
    status: string;
  } & RepairTask_Key)[];
}

export interface ListShipmentsData {
  shipments: ({
    id: UUIDString;
    trackingNumber: string;
  } & Shipment_Key)[];
}

export interface ListTechniciansData {
  technicians: ({
    id: UUIDString;
    name: string;
  } & Technician_Key)[];
}

export interface RepairTask_Key {
  id: UUIDString;
  __typename?: 'RepairTask_Key';
}

export interface Shipment_Key {
  id: UUIDString;
  __typename?: 'Shipment_Key';
}

export interface Technician_Key {
  id: UUIDString;
  __typename?: 'Technician_Key';
}

export interface UpdateAssignmentData {
  assignment_update?: Assignment_Key | null;
}

export interface UpdateAssignmentVariables {
  id: UUIDString;
  priorityLevel?: number | null;
}

export interface UpdateItemData {
  item_update?: Item_Key | null;
}

export interface UpdateItemVariables {
  id: UUIDString;
  status: string;
}

export interface UpdateRepairTaskData {
  repairTask_update?: RepairTask_Key | null;
}

export interface UpdateRepairTaskVariables {
  id: UUIDString;
  notes?: string | null;
}

export interface UpdateShipmentData {
  shipment_update?: Shipment_Key | null;
}

export interface UpdateShipmentVariables {
  id: UUIDString;
  carrierName?: string | null;
}

export interface UpdateTechnicianData {
  technician_update?: Technician_Key | null;
}

export interface UpdateTechnicianVariables {
  id: UUIDString;
  specialty?: string | null;
}

interface CreateItemRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateItemVariables): MutationRef<CreateItemData, CreateItemVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateItemVariables): MutationRef<CreateItemData, CreateItemVariables>;
  operationName: string;
}
export const createItemRef: CreateItemRef;

export function createItem(vars: CreateItemVariables): MutationPromise<CreateItemData, CreateItemVariables>;
export function createItem(dc: DataConnect, vars: CreateItemVariables): MutationPromise<CreateItemData, CreateItemVariables>;

interface UpdateItemRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateItemVariables): MutationRef<UpdateItemData, UpdateItemVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateItemVariables): MutationRef<UpdateItemData, UpdateItemVariables>;
  operationName: string;
}
export const updateItemRef: UpdateItemRef;

export function updateItem(vars: UpdateItemVariables): MutationPromise<UpdateItemData, UpdateItemVariables>;
export function updateItem(dc: DataConnect, vars: UpdateItemVariables): MutationPromise<UpdateItemData, UpdateItemVariables>;

interface DeleteItemRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteItemVariables): MutationRef<DeleteItemData, DeleteItemVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteItemVariables): MutationRef<DeleteItemData, DeleteItemVariables>;
  operationName: string;
}
export const deleteItemRef: DeleteItemRef;

export function deleteItem(vars: DeleteItemVariables): MutationPromise<DeleteItemData, DeleteItemVariables>;
export function deleteItem(dc: DataConnect, vars: DeleteItemVariables): MutationPromise<DeleteItemData, DeleteItemVariables>;

interface GetItemRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetItemVariables): QueryRef<GetItemData, GetItemVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetItemVariables): QueryRef<GetItemData, GetItemVariables>;
  operationName: string;
}
export const getItemRef: GetItemRef;

export function getItem(vars: GetItemVariables, options?: ExecuteQueryOptions): QueryPromise<GetItemData, GetItemVariables>;
export function getItem(dc: DataConnect, vars: GetItemVariables, options?: ExecuteQueryOptions): QueryPromise<GetItemData, GetItemVariables>;

interface ListItemsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListItemsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListItemsData, undefined>;
  operationName: string;
}
export const listItemsRef: ListItemsRef;

export function listItems(options?: ExecuteQueryOptions): QueryPromise<ListItemsData, undefined>;
export function listItems(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListItemsData, undefined>;

interface CreateRepairTaskRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateRepairTaskVariables): MutationRef<CreateRepairTaskData, CreateRepairTaskVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateRepairTaskVariables): MutationRef<CreateRepairTaskData, CreateRepairTaskVariables>;
  operationName: string;
}
export const createRepairTaskRef: CreateRepairTaskRef;

export function createRepairTask(vars: CreateRepairTaskVariables): MutationPromise<CreateRepairTaskData, CreateRepairTaskVariables>;
export function createRepairTask(dc: DataConnect, vars: CreateRepairTaskVariables): MutationPromise<CreateRepairTaskData, CreateRepairTaskVariables>;

interface UpdateRepairTaskRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateRepairTaskVariables): MutationRef<UpdateRepairTaskData, UpdateRepairTaskVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateRepairTaskVariables): MutationRef<UpdateRepairTaskData, UpdateRepairTaskVariables>;
  operationName: string;
}
export const updateRepairTaskRef: UpdateRepairTaskRef;

export function updateRepairTask(vars: UpdateRepairTaskVariables): MutationPromise<UpdateRepairTaskData, UpdateRepairTaskVariables>;
export function updateRepairTask(dc: DataConnect, vars: UpdateRepairTaskVariables): MutationPromise<UpdateRepairTaskData, UpdateRepairTaskVariables>;

interface DeleteRepairTaskRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteRepairTaskVariables): MutationRef<DeleteRepairTaskData, DeleteRepairTaskVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteRepairTaskVariables): MutationRef<DeleteRepairTaskData, DeleteRepairTaskVariables>;
  operationName: string;
}
export const deleteRepairTaskRef: DeleteRepairTaskRef;

export function deleteRepairTask(vars: DeleteRepairTaskVariables): MutationPromise<DeleteRepairTaskData, DeleteRepairTaskVariables>;
export function deleteRepairTask(dc: DataConnect, vars: DeleteRepairTaskVariables): MutationPromise<DeleteRepairTaskData, DeleteRepairTaskVariables>;

interface GetRepairTaskRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetRepairTaskVariables): QueryRef<GetRepairTaskData, GetRepairTaskVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetRepairTaskVariables): QueryRef<GetRepairTaskData, GetRepairTaskVariables>;
  operationName: string;
}
export const getRepairTaskRef: GetRepairTaskRef;

export function getRepairTask(vars: GetRepairTaskVariables, options?: ExecuteQueryOptions): QueryPromise<GetRepairTaskData, GetRepairTaskVariables>;
export function getRepairTask(dc: DataConnect, vars: GetRepairTaskVariables, options?: ExecuteQueryOptions): QueryPromise<GetRepairTaskData, GetRepairTaskVariables>;

interface ListRepairTasksRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListRepairTasksData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListRepairTasksData, undefined>;
  operationName: string;
}
export const listRepairTasksRef: ListRepairTasksRef;

export function listRepairTasks(options?: ExecuteQueryOptions): QueryPromise<ListRepairTasksData, undefined>;
export function listRepairTasks(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListRepairTasksData, undefined>;

interface CreateTechnicianRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateTechnicianVariables): MutationRef<CreateTechnicianData, CreateTechnicianVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateTechnicianVariables): MutationRef<CreateTechnicianData, CreateTechnicianVariables>;
  operationName: string;
}
export const createTechnicianRef: CreateTechnicianRef;

export function createTechnician(vars: CreateTechnicianVariables): MutationPromise<CreateTechnicianData, CreateTechnicianVariables>;
export function createTechnician(dc: DataConnect, vars: CreateTechnicianVariables): MutationPromise<CreateTechnicianData, CreateTechnicianVariables>;

interface UpdateTechnicianRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateTechnicianVariables): MutationRef<UpdateTechnicianData, UpdateTechnicianVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateTechnicianVariables): MutationRef<UpdateTechnicianData, UpdateTechnicianVariables>;
  operationName: string;
}
export const updateTechnicianRef: UpdateTechnicianRef;

export function updateTechnician(vars: UpdateTechnicianVariables): MutationPromise<UpdateTechnicianData, UpdateTechnicianVariables>;
export function updateTechnician(dc: DataConnect, vars: UpdateTechnicianVariables): MutationPromise<UpdateTechnicianData, UpdateTechnicianVariables>;

interface DeleteTechnicianRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteTechnicianVariables): MutationRef<DeleteTechnicianData, DeleteTechnicianVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteTechnicianVariables): MutationRef<DeleteTechnicianData, DeleteTechnicianVariables>;
  operationName: string;
}
export const deleteTechnicianRef: DeleteTechnicianRef;

export function deleteTechnician(vars: DeleteTechnicianVariables): MutationPromise<DeleteTechnicianData, DeleteTechnicianVariables>;
export function deleteTechnician(dc: DataConnect, vars: DeleteTechnicianVariables): MutationPromise<DeleteTechnicianData, DeleteTechnicianVariables>;

interface GetTechnicianRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetTechnicianVariables): QueryRef<GetTechnicianData, GetTechnicianVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetTechnicianVariables): QueryRef<GetTechnicianData, GetTechnicianVariables>;
  operationName: string;
}
export const getTechnicianRef: GetTechnicianRef;

export function getTechnician(vars: GetTechnicianVariables, options?: ExecuteQueryOptions): QueryPromise<GetTechnicianData, GetTechnicianVariables>;
export function getTechnician(dc: DataConnect, vars: GetTechnicianVariables, options?: ExecuteQueryOptions): QueryPromise<GetTechnicianData, GetTechnicianVariables>;

interface ListTechniciansRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListTechniciansData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListTechniciansData, undefined>;
  operationName: string;
}
export const listTechniciansRef: ListTechniciansRef;

export function listTechnicians(options?: ExecuteQueryOptions): QueryPromise<ListTechniciansData, undefined>;
export function listTechnicians(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListTechniciansData, undefined>;

interface CreateAssignmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateAssignmentVariables): MutationRef<CreateAssignmentData, CreateAssignmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateAssignmentVariables): MutationRef<CreateAssignmentData, CreateAssignmentVariables>;
  operationName: string;
}
export const createAssignmentRef: CreateAssignmentRef;

export function createAssignment(vars: CreateAssignmentVariables): MutationPromise<CreateAssignmentData, CreateAssignmentVariables>;
export function createAssignment(dc: DataConnect, vars: CreateAssignmentVariables): MutationPromise<CreateAssignmentData, CreateAssignmentVariables>;

interface UpdateAssignmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateAssignmentVariables): MutationRef<UpdateAssignmentData, UpdateAssignmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateAssignmentVariables): MutationRef<UpdateAssignmentData, UpdateAssignmentVariables>;
  operationName: string;
}
export const updateAssignmentRef: UpdateAssignmentRef;

export function updateAssignment(vars: UpdateAssignmentVariables): MutationPromise<UpdateAssignmentData, UpdateAssignmentVariables>;
export function updateAssignment(dc: DataConnect, vars: UpdateAssignmentVariables): MutationPromise<UpdateAssignmentData, UpdateAssignmentVariables>;

interface DeleteAssignmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteAssignmentVariables): MutationRef<DeleteAssignmentData, DeleteAssignmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteAssignmentVariables): MutationRef<DeleteAssignmentData, DeleteAssignmentVariables>;
  operationName: string;
}
export const deleteAssignmentRef: DeleteAssignmentRef;

export function deleteAssignment(vars: DeleteAssignmentVariables): MutationPromise<DeleteAssignmentData, DeleteAssignmentVariables>;
export function deleteAssignment(dc: DataConnect, vars: DeleteAssignmentVariables): MutationPromise<DeleteAssignmentData, DeleteAssignmentVariables>;

interface GetAssignmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetAssignmentVariables): QueryRef<GetAssignmentData, GetAssignmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetAssignmentVariables): QueryRef<GetAssignmentData, GetAssignmentVariables>;
  operationName: string;
}
export const getAssignmentRef: GetAssignmentRef;

export function getAssignment(vars: GetAssignmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetAssignmentData, GetAssignmentVariables>;
export function getAssignment(dc: DataConnect, vars: GetAssignmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetAssignmentData, GetAssignmentVariables>;

interface ListAssignmentsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListAssignmentsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListAssignmentsData, undefined>;
  operationName: string;
}
export const listAssignmentsRef: ListAssignmentsRef;

export function listAssignments(options?: ExecuteQueryOptions): QueryPromise<ListAssignmentsData, undefined>;
export function listAssignments(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListAssignmentsData, undefined>;

interface CreateShipmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateShipmentVariables): MutationRef<CreateShipmentData, CreateShipmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateShipmentVariables): MutationRef<CreateShipmentData, CreateShipmentVariables>;
  operationName: string;
}
export const createShipmentRef: CreateShipmentRef;

export function createShipment(vars: CreateShipmentVariables): MutationPromise<CreateShipmentData, CreateShipmentVariables>;
export function createShipment(dc: DataConnect, vars: CreateShipmentVariables): MutationPromise<CreateShipmentData, CreateShipmentVariables>;

interface UpdateShipmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateShipmentVariables): MutationRef<UpdateShipmentData, UpdateShipmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateShipmentVariables): MutationRef<UpdateShipmentData, UpdateShipmentVariables>;
  operationName: string;
}
export const updateShipmentRef: UpdateShipmentRef;

export function updateShipment(vars: UpdateShipmentVariables): MutationPromise<UpdateShipmentData, UpdateShipmentVariables>;
export function updateShipment(dc: DataConnect, vars: UpdateShipmentVariables): MutationPromise<UpdateShipmentData, UpdateShipmentVariables>;

interface DeleteShipmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteShipmentVariables): MutationRef<DeleteShipmentData, DeleteShipmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteShipmentVariables): MutationRef<DeleteShipmentData, DeleteShipmentVariables>;
  operationName: string;
}
export const deleteShipmentRef: DeleteShipmentRef;

export function deleteShipment(vars: DeleteShipmentVariables): MutationPromise<DeleteShipmentData, DeleteShipmentVariables>;
export function deleteShipment(dc: DataConnect, vars: DeleteShipmentVariables): MutationPromise<DeleteShipmentData, DeleteShipmentVariables>;

interface GetShipmentRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetShipmentVariables): QueryRef<GetShipmentData, GetShipmentVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetShipmentVariables): QueryRef<GetShipmentData, GetShipmentVariables>;
  operationName: string;
}
export const getShipmentRef: GetShipmentRef;

export function getShipment(vars: GetShipmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetShipmentData, GetShipmentVariables>;
export function getShipment(dc: DataConnect, vars: GetShipmentVariables, options?: ExecuteQueryOptions): QueryPromise<GetShipmentData, GetShipmentVariables>;

interface ListShipmentsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListShipmentsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListShipmentsData, undefined>;
  operationName: string;
}
export const listShipmentsRef: ListShipmentsRef;

export function listShipments(options?: ExecuteQueryOptions): QueryPromise<ListShipmentsData, undefined>;
export function listShipments(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListShipmentsData, undefined>;

