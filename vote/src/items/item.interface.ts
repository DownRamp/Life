import { VoteItems } from "./voteitems.interface";

// Voting option

export interface BaseItem {
    name: string;
    options: VoteItems;
    description: string;
    image: string;
    start?: Date;
    end?: Date;
}
  
export interface Item extends BaseItem {
    id: number;
}