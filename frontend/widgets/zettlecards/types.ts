export interface ZettleCardData {
  uuid: string
  card_type: 'text' | 'image' | 'url' | 'model' | 'topic'
  title: string
  text?: string
  image?: string
  url?: string
  created_at?: string
  votes?: number
  x: number
  y: number
}
