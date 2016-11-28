<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>buildings simple</Name>
    <UserStyle>
      <Title>A boring default style</Title>
      <Abstract>A sample style that just prints out a transparent red interior with a red outline</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <Name>Rule 1</Name>
          <Title>Grays fill with black Outline</Title>
          <PolygonSymbolizer>
            <Fill>
              <CssParameter name="fill">#C8C8C8</CssParameter>
            </Fill>
            <Stroke>
              <CssParameter name="stroke">#808080</CssParameter>
              <CssParameter name="stroke-width">0.5</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
        </Rule>
        </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>