<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
		xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
		xmlns="http://www.opengis.net/sld" 
		xmlns:ogc="http://www.opengis.net/ogc" 
		xmlns:xlink="http://www.w3.org/1999/xlink" 
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<!-- a named layer is the basic building block of an sld document -->

	<NamedLayer>
		<Name>Amenities_simple</Name>
		<UserStyle>
		  
			<Title>An amenitis style</Title>
			<Abstract>A sample style that just prints out a purple square</Abstract>

			<FeatureTypeStyle>
				<!--FeatureTypeName>Feature</FeatureTypeName-->
				<Rule>
					<Name>Rule 1</Name>
					<Title>Cricle</Title>

					<PointSymbolizer>
						<Graphic>
							<Mark>
								<WellKnownName>circle</WellKnownName>
								<Fill>
									<CssParameter name="fill">#649B64</CssParameter>
   								</Fill>
                                <Stroke>
                                    <CssParameter name="stroke">#808080</CssParameter>
                                    <CssParameter name="stroke-width">2</CssParameter>
                                </Stroke>
							</Mark>
							<Size>20</Size>
						</Graphic>
					</PointSymbolizer>
				</Rule>

		    </FeatureTypeStyle>
		</UserStyle>
	</NamedLayer>
</StyledLayerDescriptor>