<?xml version="1.0"?>

<st-source>
<time-stamp>From VisualWorks® NonCommercial, 7.6 of March 3, 2008 on June 6, 2009 at 4:19:18 pm</time-stamp>
<!-- Bundle TestBundle(1.0,smash)= -->


<component-property>
<name>TestBundle</name> <type>bundle</type>
<property>comment</property> <value>'TestBundle is a temporary bundle used to test the Strac plugin for Trac.  Publish it to your test repository as version 1.0 with the comment "Comment for version 1.0".'</value>
</component-property><!-- Package TestPackage1(1.0,smash)= -->


<component-property>
<name>TestPackage1</name> <type>package</type>
<property>comment</property> <value>'TestPackage1 comment here.'</value>
</component-property>

<name-space>
<name>StracTest</name>
<environment>Smalltalk</environment>
<private>false</private>
<imports>
			private Smalltalk.*
			private Core.*
			</imports>
<category>TestPackage1</category>
<attributes>
<package>TestPackage1</package>
</attributes>
</name-space>

<comment>
<name-space-id>StracTest</name-space-id>
<body>Namespaces can have comments, too!</body>
</comment>

<class>
<name>StracClass12</name>
<environment>StracTest</environment>
<super>Core.Object</super>
<private>false</private>
<indexed-type>none</indexed-type>
<inst-vars></inst-vars>
<class-inst-vars></class-inst-vars>
<imports></imports>
<category></category>
<attributes>
<package>TestPackage1</package>
</attributes>
</class>

<class>
<name>StracClass11</name>
<environment>StracTest</environment>
<super>Core.Object</super>
<private>false</private>
<indexed-type>none</indexed-type>
<inst-vars>one two </inst-vars>
<class-inst-vars></class-inst-vars>
<imports></imports>
<category></category>
<attributes>
<package>TestPackage1</package>
</attributes>
</class>

<comment>
<class-id>StracTest.StracClass11</class-id>
<body>StracClass11 has a class comment.  Hooray!

Instance Variables:
	one	&lt;Object&gt;	description of one
	two	&lt;Object&gt;	description of two

</body>
</comment>


<shared-variable>
<name>ExtraVar</name>
<environment>Core.Point</environment>
<private>false</private>
<constant>false</constant>
<category>extended</category>
<initializer>Array new: 5</initializer>
<attributes>
<package>TestPackage1</package>
</attributes>
</shared-variable>




<shared-variable>
<name>SomethingOrOther</name>
<environment>StracTest</environment>
<private>false</private>
<constant>false</constant>
<category>testing</category>
<initializer>Array new: 5</initializer>
<attributes>
<package>TestPackage1</package>
</attributes>
</shared-variable>




<methods>
<class-id>StracTest.StracClass11 class</class-id> <category>instance creation</category>

<body package="TestPackage1" selector="new">new
	"Answer a newly created and initialized instance."

	^super new initialize</body>
</methods>


<methods>
<class-id>StracTest.StracClass11</class-id> <category>initialize-release</category>

<body package="TestPackage1" selector="initialize">initialize
	"Initialize a newly created instance.  This method must answer the receiver."

	" *** Edit the following to properly initialize instance variables ***"
	one := nil.
	two := nil.
	" *** And replace this comment with additional initialization code *** "
	^self</body>
</methods>

<methods>
<class-id>StracTest.StracClass11</class-id> <category>accessing</category>

<body package="TestPackage1" selector="two">two
	^two</body>

<body package="TestPackage1" selector="two:">two: anObject
	two := anObject</body>

<body package="TestPackage1" selector="one:">one: anObject
	one := anObject</body>

<body package="TestPackage1" selector="one">one
	^one</body>
</methods>


<methods>
<class-id>Core.Object</class-id> <category>converting</category>

<body package="TestPackage1" selector="asStracObject">asStracObject
	^StracClass12 new</body>
</methods>

<!-- Package TestPackage2(1.0,smash)= -->


<component-property>
<name>TestPackage2</name> <type>package</type>
<property>comment</property> <value>'TestPackage2 comment here.'</value>
</component-property>

<class>
<name>StracClass21</name>
<environment>StracTest</environment>
<super>Core.Object</super>
<private>false</private>
<indexed-type>none</indexed-type>
<inst-vars></inst-vars>
<class-inst-vars></class-inst-vars>
<imports></imports>
<category></category>
<attributes>
<package>TestPackage2</package>
</attributes>
</class>

<shared-variable>
<name>VarName</name>
<environment>StracTest.StracClass21</environment>
<private>false</private>
<constant>false</constant>
<category>testing</category>
<initializer>Array new: 5</initializer>
<attributes>
<package>TestPackage2</package>
</attributes>
</shared-variable>




<bundle-structure>
<name>TestBundle</name> <structure>#(#(#package 'TestPackage1') #(#package 'TestPackage2'))</structure>
</bundle-structure>

<initialize>
<variable-id>Core.Point.ExtraVar</variable-id>
</initialize>

<initialize>
<variable-id>StracTest.SomethingOrOther</variable-id>
</initialize>

<initialize>
<variable-id>StracTest.StracClass21.VarName</variable-id>
</initialize>

</st-source>
