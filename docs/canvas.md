# Spatial Canvas Feature

The spatial canvas is a core feature of Recursive Garden that allows users to organize their notes in a 2D space, leveraging spatial memory for better information organization and recall.

## Features

- Infinite 2D canvas for organizing cards
- Smooth pan and zoom operations
- Drag and drop card positioning
- URL-based state management for sharing specific views
- Responsive design that works across device sizes

## Technical Implementation

### Components

- `ZettleCards.vue`: Main container component managing the infinite canvas
- `ZettleCard.vue`: Individual card component with drag functionality

### State Management

The canvas maintains several types of state:
- View position (x, y coordinates)
- Zoom level (5 distinct levels: 0.25x, 0.5x, 1x, 2x, 4x)
- Card positions (stored in database)

### URL Parameters

The canvas state is reflected in URL parameters:
- `x`: Horizontal view position
- `y`: Vertical view position
- `zoom`: Current zoom level

Example: `/cards/?x=100&y=-50&zoom=2`

### Interactions

1. **Panning**
   - Click and drag on empty canvas space
   - Updates view position
   - Maintains correct scale during pan operations

2. **Zooming**
   - Mouse wheel to zoom in/out
   - Zooms relative to cursor position
   - Maintains card positions during zoom

3. **Card Dragging**
   - Click and drag on any card
   - Updates card position in real-time
   - Saves position to database on mouse up
   - Maintains card size across zoom levels

### Performance Considerations

The implementation uses CSS transforms for:
- Smooth animations
- Hardware acceleration
- Efficient rendering of large numbers of cards

### Future Improvements

Planned enhancements include:
- Viewport-based card loading
- Spatial indexing for large card sets
- Touch/mobile support
- Collaborative features
- Minimap navigation
- Group selection and movement
- Snap-to-grid option

## Usage Examples

### Organizing by Topic
Create spatial clusters of related cards by dragging them near each other.

### Timeline Organization
Arrange cards horizontally to create timelines or sequences.

### Mind Mapping
Use the spatial canvas to create mind maps by positioning related cards in branching patterns.

### Study Zones
Create dedicated areas for different subjects or projects.

## API Reference

### Card Position Endpoint

```http
PATCH /api/cards/{uuid}/
Content-Type: application/json

{
    "x": number,
    "y": number
}
```

### Query Parameters

The cards list endpoint supports spatial queries (future implementation):

```http
GET /api/cards/?x_min=0&x_max=1000&y_min=0&y_max=1000
```