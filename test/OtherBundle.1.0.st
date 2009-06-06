<?xml version="1.0"?>

<st-source>
<time-stamp>From VisualWorks® NonCommercial, 7.6 of March 3, 2008 on June 6, 2009 at 4:20:05 pm</time-stamp>
<!-- Bundle OtherBundle(1.0,smash)= -->


<component-property>
<name>OtherBundle</name> <type>bundle</type>
<property>comment</property> <value>'OtherBundle is a temporary bundle used to test the Strac plugin for Trac.  Publish it to your test repository as version 1.0.'</value>
</component-property><!-- Package OtherPackage(1.0,smash)= -->


<component-property>
<name>OtherPackage</name> <type>package</type>
<property>comment</property> <value>'OtherPackage comment here.'</value>
</component-property>

<class>
<name>NotInTestBundle</name>
<environment>Smalltalk</environment>
<super>Core.Object</super>
<private>false</private>
<indexed-type>none</indexed-type>
<inst-vars></inst-vars>
<class-inst-vars></class-inst-vars>
<imports></imports>
<category></category>
<attributes>
<package>OtherPackage</package>
</attributes>
</class>

<comment>
<class-id>NotInTestBundle</class-id>
<body>NotInTestBundle isn't contained the the test bundle.</body>
</comment>



<bundle-structure>
<name>OtherBundle</name> <structure>#(#(#package 'OtherPackage'))</structure>
</bundle-structure>

</st-source>
