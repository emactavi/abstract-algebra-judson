<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:import href="./core/pretext-latex.xsl"/>

<!-- Suppress exercises, reading questions, and references divisions entirely -->
<xsl:template match="exercises|reading-questions|references"/>

</xsl:stylesheet>
