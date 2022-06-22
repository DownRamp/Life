import { BaseItem, Item } from "./item.interface";
import { Items } from "./items.interface";
import { Vote } from "./vote.interface";

let voters: Array<string> = [];
let items: Items = {
    1: {
      id: 1,
        name: "Food",
        options: {
            1: {
            id: 1,
            option:"Burger",
            votes:123
            }
        },
        description: "What's the best food?",
        image: "https://cdn.auth0.com/blog/whatabyte/burger-sm.png"
        },
    2: {
        id: 2,
        name: "President",
        options: {
            1: {
            id: 1,
            option:"Mr. T",
            votes:123
            }
        },        
        description: "President vote",
        image: "https://cdn.auth0.com/blog/whatabyte/pizza-sm.png"
        },
    3: {
        id: 3,
        name: "Drink",
        options: {
            1: {
            id: 1,
            option:"TEA",
            votes:123
            }
        },        description: "Informative T",
        image: "https://cdn.auth0.com/blog/whatabyte/tea-sm.png"
        }
};

export const findAll = async (): Promise<Item[]> => Object.values(items);

export const find = async (id: number): Promise<Item> => items[id];

export const create = async (newItem: BaseItem): Promise<Item> => {
    const id = new Date().valueOf();
  
    items[id] = {
      id,
      ...newItem,
    };
  
    return items[id];
  };

  export const update = async (
    id: number,
    itemUpdate: BaseItem
  ): Promise<Item | null> => {
    const item = await find(id);
  
    if (!item) {
      return null;
    }
  
    items[id] = { id, ...itemUpdate };
  
    return items[id];
  };

  export const remove = async (id: number): Promise<null | void> => {
    const item = await find(id);
  
    if (!item) {
      return null;
    }
  
    delete items[id];
  };

  export const findOption = async (id: number, ): Promise<Item> => items[id];

  export const vote = async(vote: Vote): Promise<null | void> => {
    const item = await find(vote.id);
    if (!item) {
        return null;
    }

    item.options[vote.option].votes++;
    voters.push(vote.name);
    return null;
  };