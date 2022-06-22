export interface BaseVoteItem{
    option: string;
    votes: number;
}

export interface VoteItem extends BaseVoteItem {
    id: number;
}